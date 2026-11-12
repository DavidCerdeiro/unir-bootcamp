"""Cliente OpenAI conectado al servidor MCP local.

Flujo: descubre las herramientas del servidor MCP, se las presenta al modelo
como function tools de la API de Chat Completions y, cuando el modelo pide una llamada,
la ejecuta contra el servidor MCP y devuelve el resultado al modelo. Asi el
modelo puede encadenar llamadas secuenciales (p. ej. geocode_city y despues
get_current_weather) hasta poder responder al usuario.
"""

import asyncio
import json
import logging

from fastmcp import Client as MCPClient
from openai import (
    AsyncOpenAI, 
    APIConnectionError, 
    RateLimitError, 
    APIError, 
    InternalServerError, 
    APITimeoutError
)

from config import settings

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "Eres un asistente financiero y meteorologico en español. Usa las "
    "herramientas disponibles para responder con datos reales y actuales. "
    "Para el clima de una ciudad, primero llama a geocode_city para obtener "
    "sus coordenadas y despues a get_current_weather o get_weather_forecast. "
    "Responde de forma clara y breve, indicando unidades."
)

MAX_TOOL_ROUNDS = 8
MAX_RETRIES = 3


class MCPOpenAIClient:
    """Orquesta la conversacion entre el usuario, OpenAI y el servidor MCP."""

    def __init__(self, mcp_url: str = settings.MCP_URL, model: str = settings.OPENAI_MODEL) -> None:
        self.model = model
        self.openai = AsyncOpenAI()  # Cliente asíncrono para no bloquear el event loop
        self.mcp = MCPClient(mcp_url)
        self.tools: list[dict] = []
        self._history: list = [
            {"role": "system", "content": SYSTEM_PROMPT},  # Rol 'system' o 'developer' soportado por OpenAI
        ]

    async def __aenter__(self) -> "MCPOpenAIClient":
        await self.mcp.__aenter__()
        await self._load_tools()
        return self

    async def __aexit__(self, *exc_info) -> None:
        await self.mcp.__aexit__(*exc_info)

    async def _load_tools(self) -> None:
        """Descubre las herramientas MCP y las convierte a function tools."""
        mcp_tools = await self.mcp.list_tools()
        self.tools = []
        
        for tool in mcp_tools:
            self.tools.append({
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.inputSchema
                }
            })
            logger.info(f"Herramienta cargada: {tool.name}")

    def tool_names(self) -> list[str]:
        # Ajustado al esquema estándar de OpenAI donde 'name' está dentro de 'function'
        return [tool["function"]["name"] for tool in self.tools]

    async def ask(self, user_text: str) -> str:
        """Ejecuta un turno completo: usuario -> modelo -> herramientas -> respuesta."""
        
        # 1. Añade el mensaje del usuario al historial
        self._history.append({"role": "user", "content": user_text})
        
        # 2. Bucle de llamadas (máximo MAX_TOOL_ROUNDS)
        for _ in range(MAX_TOOL_ROUNDS):
            response = None
            
            # a. Reintentos ante errores transitorios ampliados
            for attempt in range(MAX_RETRIES):
                try:
                    response = await self.openai.chat.completions.create(
                        model=self.model,
                        messages=self._history,
                        tools=self.tools,
                        tool_choice="auto"
                    )
                    break
                except (APIConnectionError, RateLimitError, APIError, InternalServerError, APITimeoutError) as e:
                    logger.warning(f"Fallo temporal con OpenAI (intento {attempt+1}/{MAX_RETRIES}): {e}")
                    if attempt == MAX_RETRIES - 1:
                        return "Lo siento, hay problemas de conexión o inestabilidad con el servicio de inteligencia artificial. Inténtalo de nuevo más tarde."
                    await asyncio.sleep(2 ** attempt)
            
            if not response:
                return "Error crítico al contactar con OpenAI."

            message = response.choices[0].message
            
            # b. Añade los items de salida al historial
            self._history.append(message.model_dump(exclude_none=True))
            
            # c. Si no hay function calls, devuelve el texto de respuesta
            if not message.tool_calls:
                return message.content or ""
                
            # d. Para cada function call, ejecuta la herramienta localmente
            for tool_call in message.tool_calls:
                if tool_call.type == "function":
                    func_name = tool_call.function.name
                    func_args = tool_call.function.arguments
                    
                    logger.info(f"El modelo solicita ejecutar: {func_name}")
                    result_text = await self._run_mcp_tool(func_name, func_args)
                    
                    # Añade el resultado de la herramienta al historial (esquema oficial OpenAI)
                    self._history.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": func_name,
                        "content": result_text
                    })
        
        return "Se ha superado el límite de operaciones automáticas. Por favor, sé más específico."

    async def _run_mcp_tool(self, name: str, arguments: str) -> str:
        """Ejecuta una herramienta en el servidor MCP y devuelve el resultado como texto."""
        try:
            # Parsea el string JSON proporcionado por el modelo
            args_dict = json.loads(arguments) if arguments else {}
            
            # Ejecuta la herramienta en el servidor MCP local
            result = await self.mcp.call_tool(name, arguments=args_dict)
            
            # FastMCP devuelve una lista de TextContent/ImageContent.
            # Extraemos y concatenamos solo la parte textual.
            if hasattr(result, "content"):
                return "\n".join(c.text for c in result.content if getattr(c, "type", "") == "text")
            
            # Fallback en caso de que la implementación devuelva estructuras más simples
            elif isinstance(result, str):
                return result
            else:
                return json.dumps(result)
                
        except json.JSONDecodeError:
            return "Error: Los argumentos proporcionados por la IA no son un JSON válido."
        except Exception as e:
            logger.error(f"Fallo al ejecutar herramienta {name} en MCP: {e}")
            return f"Error ejecutando la herramienta localmente: {str(e)}"
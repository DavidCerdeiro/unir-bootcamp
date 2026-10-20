"""Lógica principal del chatbot: conexión con Ollama y modelo local gemma3:1b."""

import ollama
from core.conversation import Conversation

MODEL = "gemma3:1b"

class OllamaNoDisponibleError(Exception):
    """El servicio de Ollama no responde o el modelo no está descargado."""
    pass

class Chatbot:
    """Chatbot que conversa con el modelo local gemma3:1b vía Ollama SDK.

    Funciona completamente offline: solo necesita el servicio local de
    Ollama arrancado y el modelo descargado (ollama pull gemma3:1b).
    """

    def __init__(self, conversation: Conversation | None = None, model: str = MODEL) -> None:
        self.conversation = conversation or Conversation()
        self.model = model

    def check_model_available(self) -> None:
        """Comprueba que Ollama responde y que el modelo está descargado."""
        try:
            # Lista los modelos locales disponibles
            response = ollama.list()
            
            # Compatibilidad con distintas versiones del SDK de Python de Ollama
            models = response.get('models', []) if isinstance(response, dict) else response.models
            model_names = [m.get('model', m.get('name', '')) if isinstance(m, dict) else m.model for m in models]
            
            # Validamos si nuestro modelo (o su alias latest) está en la lista
            if self.model not in model_names and f"{self.model}:latest" not in model_names:
                raise OllamaNoDisponibleError(
                    f"El modelo '{self.model}' no está descargado.\n"
                    f"Por favor, ejecuta en tu terminal: ollama pull {self.model}"
                )
        except Exception as e:
            if isinstance(e, OllamaNoDisponibleError):
                raise
            # Captura ConnectionError u otros fallos si el servicio no está levantado
            raise OllamaNoDisponibleError(
                "El servicio local de Ollama no responde. Asegúrate de que "
                "la aplicación de Ollama está ejecutándose en tu sistema."
            ) from e

    def ask(self, user_text: str) -> str:
        """Envía la pregunta al modelo manteniendo el contexto del diálogo."""
        self.conversation.add_user(user_text)
        
        full_response = ""
        try:
            # Llamamos a ollama en modo streaming pasándole el historial completo
            stream = ollama.chat(
                model=self.model,
                messages=self.conversation.messages,
                stream=True
            )
            
            # Procesamos el generador stream y lo mostramos al instante en consola
            for chunk in stream:
                content = chunk['message']['content']
                print(content, end='', flush=True)
                full_response += content
                
            print() # Salto de línea limpio cuando termina la respuesta
            
        except Exception as e:
            raise OllamaNoDisponibleError(
                f"Se interrumpió la comunicación con Ollama: {str(e)}"
            ) from e
            
        # Almacenamos la respuesta completa devuelta para futuros contextos
        self.conversation.add_assistant(full_response)
        
        return full_response
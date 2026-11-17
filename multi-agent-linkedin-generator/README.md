# 🤖 Multi-Agent LinkedIn Post Generator CLI

Un chatbot interactivo de terminal impulsado por el **OpenAI Agents SDK**. Este proyecto implementa una arquitectura multi-agente para generar publicaciones de LinkedIn altamente especializadas y estructuradas, garantizando un tono adecuado según el nicho tecnológico, de marketing o legal.

Este proyecto forma parte de mi portfolio de soluciones desarrolladas durante el bootcamp, demostrando capacidades avanzadas en orquestación de LLMs, manejo de contexto y salidas estructuradas.

## 🚀 Características Principales

- **Arquitectura Multi-Agente (Handoffs):** Un Agente Principal (Triage) analiza la intención del usuario y transfiere dinámicamente la conversación al especialista adecuado.
- **Especialización por Dominio:** Cuenta con agentes preconfigurados con "system prompts" específicos para:
  - 📈 Marketing, ventas y marca personal.
  - 💻 Programación y desarrollo de software.
  - ⚖️ Sector jurídico-legal y compliance.
- **Salidas Estructuradas (Pydantic):** Integración nativa con Pydantic para forzar a que el LLM devuelva siempre una estructura de datos predecible (`LinkedinPost` con `title`, `content`, `hashtags`, y `category`).
- **Memoria de Conversación:** Mantiene el contexto de la charla a lo largo de los turnos utilizando la gestión de historial del SDK.
- **Interfaz CLI Interactiva:** Interfaz limpia en terminal con indicadores visuales de qué agente está procesando la solicitud en cada momento.

## 🏗️ Estructura del Proyecto

```text
├── main.py                     # Punto de entrada y bucle CLI interactivo
├── post_agents/                
│   ├── main_agent.py           # Lógica de triage y delegación (Router)
│   └── specialized_agents.py   # Modelos Pydantic y agentes especialistas
├── core/
│   ├── chatbot.py              # Ejecución del turno (Runner) y renderizado UI
│   └── conversation.py         # Gestión del estado e historial de mensajes
├── requirements.txt            # Dependencias del proyecto
└── .env                        # Variables de entorno (API Keys)
```
*(Nota: El directorio de agentes se denomina `post_agents` para evitar colisiones de namespace con la librería nativa `agents` de OpenAI).*

## 🛠️ Tecnologías Utilizadas

- **Python 3.10+**
- **OpenAI Agents SDK:** Para la orquestación, flujos de trabajo y handoffs entre agentes.
- **Pydantic:** Para la validación de datos y "Structured Outputs".
- **Modelos de OpenAI:** Uso de `gpt-4o-mini` (o equivalente) para inferencia rápida y eficiente.

## ⚙️ Puesta en marcha

1. Clona el repositorio y navega al directorio del proyecto:
```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_DIRECTORIO>
```

2. Crea y activa un entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

4. Configura tus credenciales creando un archivo `.env` en la raíz del proyecto:
```env
OPENAI_API_KEY=tu_clave_de_openai_aqui
```

5. Inicia la aplicación:
```bash
python main.py
```

## 💡 Ejemplo de Uso

```text
Usuario: Escribe un post sobre las ventajas de usar microservicios en Python.

🤖 [Agente Principal] está respondiendo...
🤖 [Agente de Programación] está respondiendo...

============================================================
📌 TÍTULO: Por qué los microservicios en Python están cambiando las reglas del juego 🚀
📁 CATEGORÍA: DESARROLLO DE SOFTWARE
------------------------------------------------------------
(Contenido estructurado del post generado por el especialista técnico...)
------------------------------------------------------------
🏷️ HASHTAGS: #Python #Microservicios #ArquitecturaDeSoftware #Backend
============================================================
```
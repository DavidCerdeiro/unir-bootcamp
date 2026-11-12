# 🌐 Servidor MCP + Cliente OpenAI (Finanzas y Clima)

Este proyecto es una implementación completa del **Model Context Protocol (MCP)** utilizando `FastMCP`. Consiste en una arquitectura cliente-servidor donde un cliente interactivo por CLI (potenciado por la API de OpenAI) se conecta a un servidor local MCP que expone herramientas de integración con APIs públicas del mundo real.

Desarrollado como parte del portfolio de ingeniería de software (Bootcamp UNIR), este proyecto demuestra habilidades avanzadas en el manejo de **Function Calling (Tool Calling)**, orquestación de llamadas secuenciales de LLMs, y arquitecturas de red locales mediante transporte HTTP.

## ✨ Características Principales

El servidor expone 5 herramientas funcionales divididas en dos dominios:

💰 **Módulo Financiero (ExchangeRate-API)**
- `convert_currency`: Conversión precisa entre dos divisas.
- `get_exchange_rates`: Consulta de tasas de cambio frente a una moneda base.

🌤️ **Módulo Meteorológico (Open-Meteo)**
- `geocode_city`: Geocodificación directa (Ciudad → Coordenadas Lat/Lon).
- `get_current_weather`: Consulta del clima actual basado en coordenadas.
- `get_weather_forecast`: Pronóstico meteorológico de hasta 7 días.

🤖 **Orquestación de IA**
- **Llamadas Secuenciales**: El modelo es capaz de razonar que, para pedir el clima de "Madrid", primero debe invocar `geocode_city("Madrid")` y pasar dinámicamente esas coordenadas a `get_current_weather(lat, lon)`.
- **Manejo de Errores**: Sistema robusto con validación tipada, captura de timeouts, límites de cuota (RateLimit) y reintentos automáticos.

## 🏗️ Arquitectura del Proyecto

```text
├── server/
│   ├── mcp_server.py           # Configuración de FastMCP e inyección de dependencias
│   ├── currency_tools.py       # Lógica y validación de conversión de divisas
│   ├── weather_tools.py        # Lógica y validación meteorológica
│   ├── geocoding_tools.py      # Lógica de geolocalización
│   └── api_clients.py          # Clientes HTTP aislados para Open-Meteo y ExchangeRate
├── client/
│   ├── openai_client.py        # Orquestador del LLM, formateo de tools y bucle
│   └── cli_interface.py        # Interfaz de línea de comandos iterativa
├── main_server.py              # Punto de entrada (Servidor HTTP)
├── main_client.py              # Punto de entrada (Cliente CLI)
├── requirements.txt            # Dependencias del proyecto
└── .env.example                # Plantilla de variables de entorno
```

## ⚙️ Variables de Entorno

El proyecto utiliza variables de entorno para su configuración. Debes crear un archivo `.env` en la raíz del proyecto (puedes basarte en `.env.example`). 

**Variables requeridas para el Cliente:**
* `OPENAI_API_KEY`: Tu clave de la API de OpenAI (Obligatoria).
* `OPENAI_MODEL`: El modelo a utilizar (por defecto `gpt-4o-mini`).
* `MCP_URL`: La dirección de tu servidor MCP local (por defecto `http://127.0.0.1:8000`).

**Variables para el Servidor MCP:**
* `API_KEY_EXCHANGE`: Clave para ExchangeRate-API. Puedes obtener una gratuita registrándote en [su web oficial](https://www.exchangerate-api.com/). *Si la omites, el servidor usará automáticamente el endpoint abierto público de la API como plan de contingencia.*
* Open-Meteo no requiere configuración ni API Keys ya que es 100% gratuita.
* `HTTP_TIMEOUT`: Tiempo límite de espera para peticiones HTTP (por defecto `10` segundos).

## 🚀 Instalación y Puesta en Marcha

1. **Clonar el repositorio y preparar el entorno**
   ```bash
   git clone <tu-repositorio>
   cd <carpeta-del-proyecto>
   python -m venv .venv
   
   # Activar entorno virtual
   source .venv/bin/activate   # En Linux/macOS
   .venv\Scripts\activate      # En Windows
   
   pip install -r requirements.txt
   ```

2. **Configurar Variables de Entorno**
   Copia el archivo de ejemplo para crear tu configuración local:
   ```bash
   cp .env.example .env
   ```
   Abre el archivo `.env` y añade tu `OPENAI_API_KEY` y opcionalmente tu `API_KEY_EXCHANGE`.

3. **Ejecutar el entorno (Requiere dos terminales)**

   * **Terminal 1 (Servidor):**
     Inicia el servidor MCP local que expondrá las herramientas.
     ```bash
     python main_server.py
     ```
     *(Verás un log indicando que el servidor escucha en http://127.0.0.1:8000)*

   * **Terminal 2 (Cliente):**
     Inicia la interfaz de línea de comandos para interactuar con la IA.
     ```bash
     python main_client.py
     ```

## 💻 Uso de la CLI (Ejemplos)

Una vez iniciada la CLI, puedes realizar consultas en lenguaje natural:

- **Finanzas:** *"Convierte 150 USD a EUR"* o *"Dime cómo está el Yen japonés frente al Euro hoy"*
- **Clima Secuencial:** *"¿Qué tiempo hace ahora mismo en Tokio?"* (La IA geocodificará Tokio primero y luego pedirá el clima).
- **Comandos del sistema:**
  * `/ayuda`: Muestra las capacidades del asistente.
  * `/salir`: Cierra la aplicación de forma segura.
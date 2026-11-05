# Laboratorio RAG: Chatbot Corporativo CLI (LangChain & OpenAI)

Este proyecto forma parte de la colección de laboratorios prácticos desarrollados durante la formación en UNIR. Consiste en la implementación de un sistema RAG (Retrieval-Augmented Generation) funcional a través de una interfaz de línea de comandos (CLI). 

El objetivo principal es construir un asistente conversacional capaz de responder preguntas basándose **exclusivamente** en el contexto proporcionado por una serie de documentos internos de una empresa ficticia, evitando alucinaciones y el uso de conocimiento externo del modelo.

## 🚀 Tecnologías y Arquitectura

El sistema está construido en Python siguiendo una arquitectura modular y utiliza el ecosistema de LangChain para la orquestación de LLMs:

* **LangChain Core & Community**: Orquestación del flujo RAG (carga, división, recuperación y generación).
* **OpenAI API**: 
  * *Embeddings*: `text-embedding-3-small` para la vectorización semántica de los documentos.
  * *Generación*: `gpt-4o` (o superior) para la inferencia y generación de respuestas en lenguaje natural.
* **Vector Store**: `InMemoryVectorStore` para el almacenamiento temporal y búsqueda por similitud de los vectores.
* **Text Splitter**: `RecursiveCharacterTextSplitter` para trocear los documentos Markdown preservando la coherencia de los párrafos.

## 📁 Estructura del Proyecto

```text
├── main.py              # Punto de entrada de la aplicación e interfaz CLI
├── requirements.txt     # Dependencias del proyecto
├── .env                 # Variables de entorno (API Keys) - No versionado
├── README.md            # Documentación del laboratorio
├── documents/           # Base de conocimiento (Data Source)
│   ├── documento1.md    # Información corporativa ficticia (Historia, visión, servicios)
│   └── documento2.md    # Políticas internas y procedimientos (Horarios, beneficios)
└── core/                # Lógica de negocio
    ├── __init__.py
    ├── rag_system.py    # Motor RAG: Carga, Text Splitting y Retrieval semántico
    └── chatbot.py       # Lógica conversacional, inyección de contexto y memoria
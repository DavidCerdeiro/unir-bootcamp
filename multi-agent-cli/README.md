# Chatbot de expertos tematicos con Ollama (plantilla)

Plantilla del reto: chatbot de consola con tres expertos tematicos (Programacion,
Marketing y Juridico-Legal) sobre el modelo local `gemma3:1b` via Ollama SDK,
funcionando completamente offline.

La estructura ya esta creada; busca los `TODO` en el codigo:

- `experts/expert_prompts.py`: escribe los prompts de sistema de los tres expertos.
- `core/conversation.py`: historial, contexto y cambio de experto.
- `core/chatbot.py`: conexion con Ollama SDK (streaming) y manejo de errores.
- `main.py`: completa los comandos `/experto` y `/reiniciar` (el menu y el bucle ya funcionan).

## Requisitos previos

1. Tener instalado [Ollama](https://ollama.com) y el servicio arrancado
   (la aplicacion de escritorio o `ollama serve`).
2. Descargar el modelo local:

```bash
ollama pull gemma3:1b
```

## Puesta en marcha

```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

La plantilla arranca desde el principio: veras avisos `[plantilla] TODO` en las
partes que faltan por implementar.

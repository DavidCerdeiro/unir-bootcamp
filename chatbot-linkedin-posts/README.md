# Generador de posts de LinkedIn con salidas estructuradas (plantilla)

Plantilla del reto: chatbot de terminal que genera posts de LinkedIn usando la API
de OpenAI con Structured Outputs (`responses.parse()`) y un modelo Pydantic
(`LinkedinPost`) con validacion estricta.

La estructura ya esta creada; busca los `TODO` en el codigo:

- `models/linkedin_post.py`: define los campos del modelo y la validacion estricta.
- `core/api_client.py`: llamada con `responses.parse()`, `text_format` y refusals.
- `core/chatbot.py`: manejo de errores y visualizacion organizada del resultado.

`main.py` (el bucle por terminal) ya funciona: puedes ejecutarlo desde el principio
y veras los avisos de las partes que faltan por implementar.

## Puesta en marcha

1. Crea y activa un entorno virtual e instala dependencias:

```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

2. Crea un archivo `.env` en la raiz del proyecto (no lo subas a git):

```
OPENAI_API_KEY=tu_clave
```

3. Ejecuta la aplicacion:

```bash
python main.py
```

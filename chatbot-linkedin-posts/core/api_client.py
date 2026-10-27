"""Cliente de OpenAI: llamada con Structured Outputs y manejo de rechazos."""

from openai import OpenAI

from models.linkedin_post import LinkedinPost

MODEL = "gpt-4.1"

SYSTEM_PROMPT = (
    "Eres un experto en comunicacion profesional en LinkedIn. A partir de la idea "
    "del usuario, genera un post en español con tono profesional y cercano. "
    "Devuelve titulo, contenido, hashtags (sin el simbolo #) y categoria tematica."
)


class RechazoAPIError(Exception):
    """El modelo ha rechazado generar el contenido solicitado (refusal)."""


class OpenAIClient:
    """Encapsula la llamada a la API Responses con salidas estructuradas."""

    def __init__(self, model: str = MODEL) -> None:
        # El cliente lee OPENAI_API_KEY del entorno (cargado desde .env).
        self.client = OpenAI()
        self.model = model

    def generar_post(self, idea: str) -> LinkedinPost:
        """Genera un post de LinkedIn validado contra el modelo Pydantic."""
        
        # 1. Llamada a la API usando la sintaxis requerida
        response = self.client.responses.parse(
            model=self.model,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": idea}
            ],
            text_format=LinkedinPost
        )

        # 2. Iteración sobre response.output para detectar refusals
        for item in response.output:
            if getattr(item, "type", "") == "message" and hasattr(item, "parts"):
                for part in item.parts:
                    if getattr(part, "type", "") == "refusal":
                        raise RechazoAPIError(part.refusal)

        # 3. Validación final del objeto parseado
        if response.output_parsed is None:
            raise RechazoAPIError("La API no devolvió una salida estructurada válida.")

        # 4. Retorno del objeto LinkedinPost ya validado
        return response.output_parsed
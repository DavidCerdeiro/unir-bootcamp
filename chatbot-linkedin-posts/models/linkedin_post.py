"""Modelo Pydantic del post de LinkedIn con validacion estricta."""

from pydantic import BaseModel, ConfigDict

class LinkedinPost(BaseModel):
    """Post de LinkedIn generado por la IA."""

    # Configuración estricta para prohibir propiedades adicionales
    # Esto asegura que OpenAI devuelva exactamente esta estructura y nada más
    model_config = ConfigDict(extra="forbid")

    title: str
    content: str
    hashtags: list[str]
    category: str
"""Logica principal del chatbot: entrada por terminal, llamada y visualizacion."""

import openai
from pydantic import ValidationError

from core.api_client import OpenAIClient, RechazoAPIError
from models.linkedin_post import LinkedinPost


class Chatbot:
    """Chatbot de terminal que genera posts de LinkedIn estructurados."""

    def __init__(self, api_client: OpenAIClient | None = None) -> None:
        self.api_client = api_client or OpenAIClient()

    def pedir_idea(self) -> str:
        """Solicita al usuario la idea del post por terminal."""
        return input("\nDescribe la idea de tu post de LinkedIn (o 'salir'): ").strip()

    def procesar(self, idea: str) -> LinkedinPost | None:
        """Genera el post y gestiona los errores informando con claridad."""
        print("Generando post... ⏳\n")
        try:
            return self.api_client.generar_post(idea)
        
        except RechazoAPIError as e:
            print(f"❌ El modelo ha rechazado la solicitud (Refusal): {e}")
        except openai.LengthFinishReasonError:
            print("❌ Error: Se alcanzó el límite máximo de tokens. El post quedó incompleto.")
        except ValidationError as e:
            print(f"❌ Error de esquema: La IA no devolvió el formato esperado por Pydantic.\nDetalles: {e}")
        except openai.APIConnectionError:
            print("❌ Error de red: No se pudo conectar a los servidores de OpenAI. Revisa tu conexión.")
        except openai.APIError as e:
            print(f"❌ Error genérico de la API de OpenAI:\n{e}")
        except Exception as e:
            print(f"❌ Ha ocurrido un error inesperado:\n{e}")
        
        # Si cae en cualquier except, devuelve None
        return None

    def mostrar(self, post: LinkedinPost) -> None:
        """Muestra los campos del post validado de forma organizada."""
        
        # Añadimos el prefijo '#' a los hashtags, ya que le pedimos a la API que nos los diera sin él
        hashtags_formateados = " ".join([f"#{tag}" for tag in post.hashtags])

        print("=" * 60)
        print(f"📌 TÍTULO:    {post.title}")
        print(f"📂 CATEGORÍA: {post.category}")
        print("-" * 60)
        print(post.content)
        print("-" * 60)
        print(f"🏷️ HASHTAGS:  {hashtags_formateados}")
        print("=" * 60)
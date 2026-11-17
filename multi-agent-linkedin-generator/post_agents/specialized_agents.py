"""Agentes especializados por tematica y modelo Pydantic de la publicacion.

Nota sobre la estructura: el enunciado sugiere una carpeta agents/, pero ese
nombre colisiona con el modulo agents del propio OpenAI Agents SDK (romperia
los imports), asi que el paquete local se llama post_agents/.
"""

from agents import Agent
from pydantic import BaseModel, Field

MODEL = "gpt-4.1-mini" # Ajusta el modelo según lo que tengas configurado


class LinkedinPost(BaseModel):
    """Estructura común de toda publicación generada."""
    title: str = Field(description="Título atractivo de la publicación para LinkedIn.")
    content: str = Field(description="Contenido principal del post, estructurado y profesional.")
    hashtags: list[str] = Field(description="Lista de hashtags relevantes (ej. ['#Marketing', '#Ventas']).")
    category: str = Field(description="Categoría temática de la publicación.")


marketing_agent = Agent(
    name="Agente de Marketing",
    instructions=(
        "Eres un experto en marketing digital, ventas y branding personal para LinkedIn. "
        "Genera publicaciones atractivas, persuasivas y profesionales sobre estos temas, "
        "centradas en aportar valor y generar engagement. "
        "Siempre debes responder generando un objeto estructurado que cumpla con la estructura requerida."
    ),
    handoff_description="Útil para solicitudes sobre marketing, publicidad, ventas, SEO, estrategias de mercado o marca personal.",
    model=MODEL,
    output_type=LinkedinPost
)

programacion_agent = Agent(
    name="Agente de Programación",
    instructions=(
        "Eres un desarrollador de software Senior que comparte conocimientos técnicos en LinkedIn. "
        "Genera publicaciones sobre desarrollo, buenas prácticas de código, arquitectura de software, "
        "lenguajes de programación o herramientas tecnológicas. El tono debe ser técnico pero accesible. "
        "Siempre debes responder generando un objeto estructurado que cumpla con la estructura requerida."
    ),
    handoff_description="Útil para solicitudes sobre código, programación, desarrollo de software, arquitectura IT o tecnologías concretas.",
    model=MODEL,
    output_type=LinkedinPost
)

juridico_agent = Agent(
    name="Agente Jurídico",
    instructions=(
        "Eres un abogado especialista en derecho corporativo y cumplimiento normativo. "
        "Genera publicaciones formales, precisas y rigurosas sobre temas legales, nuevas leyes, "
        "compliance o consejos jurídicos para empresas y profesionales. "
        "Siempre debes responder generando un objeto estructurado que cumpla con la estructura requerida."
    ),
    handoff_description="Útil para solicitudes sobre leyes, derecho, normativas, contratos legales o compliance corporativo.",
    model=MODEL,
    output_type=LinkedinPost
)


SPECIALIZED_AGENTS = [a for a in (marketing_agent, programacion_agent, juridico_agent) if a]
"""Logica principal del chatbot: ejecuta el agente principal y muestra el resultado."""

from agents import Runner
from core.conversation import Conversation
from post_agents.main_agent import main_agent
from post_agents.specialized_agents import LinkedinPost

class Chatbot:
    """Chatbot de terminal sobre el OpenAI Agents SDK."""

    def __init__(self) -> None:
        self.conversation = Conversation()

    def ask(self, user_text: str) -> None:
        """Ejecuta un turno completo."""
        # 1. Prepara los datos de entrada uniendo historial y mensaje actual
        entrada = self.conversation.input_for(user_text)

        # Ejecuta el flujo del agente sincrónicamente
        result = Runner.run_sync(main_agent, entrada)

        # 2. Actualiza el historial tras la ejecución
        self.conversation.update(result)

        # 3. Muestra visualmente qué agente tomó el control y respondió
        print(f"\n🤖 [{result.last_agent.name}] está respondiendo...")

        # 4. Comprueba si el resultado es nuestra estructura Pydantic de LinkedIn
        if isinstance(result.final_output, LinkedinPost):
            self._mostrar_post(result.final_output)
        else:
            # Si es una cadena normal (ej. pidiendo aclaración), se imprime tal cual
            print(f"\n{result.final_output}\n")

    @staticmethod
    def _mostrar_post(post: LinkedinPost) -> None:
        """Muestra los campos del post de forma organizada en la terminal."""
        print("\n" + "=" * 60)
        print(f"📌 TÍTULO: {post.title}")
        print(f"📁 CATEGORÍA: {post.category.upper()}")
        print("-" * 60)
        print(f"{post.content}")
        print("-" * 60)
        
        # Formateamos los hashtags asegurando que lleven '#' al inicio
        hashtags_formateados = " ".join([h if h.startswith("#") else f"#{h}" for h in post.hashtags])
        print(f"🏷️  HASHTAGS: {hashtags_formateados}")
        print("=" * 60 + "\n")
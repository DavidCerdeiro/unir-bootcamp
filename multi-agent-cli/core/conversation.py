"""Gestión del historial y del estado de la conversación."""

class Conversation:
    """Mantiene el historial de mensajes y el experto activo."""

    def __init__(self) -> None:
        self._system_prompt: str | None = None
        self._history: list[dict] = []

    @property
    def messages(self) -> list[dict]:
        """Historial completo listo para enviar al modelo (sistema + diálogo)."""
        msgs = []
        # Ollama espera el contexto del sistema como el primer mensaje
        if self._system_prompt:
            msgs.append({"role": "system", "content": self._system_prompt})
        
        # Añadimos todo el historial de la conversación actual
        msgs.extend(self._history)
        return msgs

    def set_expert(self, system_prompt: str, keep_history: bool = True) -> None:
        """Activa un experto, conservando o reiniciando el historial."""
        self._system_prompt = system_prompt
        if not keep_history:
            self.reset()

    def add_user(self, content: str) -> None:
        """Añade el mensaje del usuario al historial."""
        self._history.append({"role": "user", "content": content})

    def add_assistant(self, content: str) -> None:
        """Añade la respuesta del asistente al historial."""
        self._history.append({"role": "assistant", "content": content})

    def reset(self) -> None:
        """Reinicia el diálogo conservando el experto activo."""
        self._history.clear()
"""Gestion del historial de la conversacion entre turnos."""

class Conversation:
    """Mantiene el historial en el formato de items del Agents SDK.

    El Runner devuelve en cada turno la lista completa de items de entrada
    para el siguiente turno (result.to_input_list()).
    """

    def __init__(self) -> None:
        self._items: list = []

    def input_for(self, user_text: str) -> list:
        """Historial previo + el nuevo mensaje del usuario, listo para el Runner."""
        nuevo_mensaje = {"role": "user", "content": user_text}
        # Retornamos el historial actual concatenado con el nuevo mensaje
        return self._items + [nuevo_mensaje]

    def update(self, result) -> None:
        """Guarda el estado devuelto por el Runner tras un turno."""
        # Se actualiza el historial interno con toda la traza devuelta por el agente
        self._items = result.to_input_list()
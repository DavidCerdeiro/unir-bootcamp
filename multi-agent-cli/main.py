"""Punto de entrada: chatbot de expertos temáticos con Ollama y gemma3:1b."""

from core.chatbot import Chatbot, OllamaNoDisponibleError
from core.conversation import Conversation
from experts.expert_prompts import EXPERTS

COMANDOS = "/experto (cambiar de experto) | /reiniciar (borrar diálogo) | /salir"


def elegir_experto() -> dict | None:
    """Muestra el menú de expertos y devuelve el elegido (None para salir)."""
    print("\nExpertos disponibles:")
    for opcion, experto in EXPERTS.items():
        print(f"  {opcion}. {experto['name']}")
    print("  0. Salir")

    while True:
        opcion = input("Elige experto (número): ").strip()
        if opcion == "0":
            return None
        if opcion in EXPERTS:
            return EXPERTS[opcion]
        print("Opción no válida. Prueba otra vez.")


def main() -> None:
    print("=" * 62)
    print("Chatbot de expertos temáticos con Ollama (modelo local gemma3:1b)")
    print("Funciona 100% offline con el servicio local de Ollama.")
    print("=" * 62)

    conversation = Conversation()
    chatbot = Chatbot(conversation)

    # 1. Comprobamos que el modelo y Ollama estén listos
    try:
        chatbot.check_model_available()
    except OllamaNoDisponibleError as error:
        print(f"\n[Error] {error}")
        return

    # 2. Selección inicial de experto
    experto = elegir_experto()
    if experto is None:
        print("Hasta pronto.")
        return

    conversation.set_expert(experto["system_prompt"])
    print(f"\nExperto activo: {experto['name']}")
    print(f"Comandos: {COMANDOS}")

    # 3. Bucle de conversación
    while True:
        try:
            user_text = input(f"\n[{experto['name']}] Tú: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nHasta pronto.")
            break

        if not user_text:
            continue

        # Comando: Salir
        if user_text.lower() == "/salir":
            print("Hasta pronto.")
            break

        # Comando: Reiniciar
        if user_text.lower() == "/reiniciar":
            conversation.reset()
            print(f"[Sistema] Historial borrado. {experto['name']} está listo para una nueva consulta.")
            continue

        # Comando: Cambiar Experto
        if user_text.lower() == "/experto":
            nuevo_experto = elegir_experto()
            if nuevo_experto is None:
                print("Hasta pronto.")
                break
            
            # Preguntamos si se desea conservar el contexto
            mantener = input("¿Deseas mantener el historial de la conversación actual? (s/n): ").strip().lower()
            keep_history = (mantener == 's')
            
            conversation.set_expert(nuevo_experto["system_prompt"], keep_history=keep_history)
            experto = nuevo_experto
            
            estado_historial = "conservado" if keep_history else "reiniciado"
            print(f"\n[Sistema] Cambiado a {experto['name']} (Historial {estado_historial}).")
            print(f"Comandos: {COMANDOS}")
            continue

        # Interacción con el chatbot
        print(f"{experto['name']}: ", end="", flush=True)
        try:
            chatbot.ask(user_text)
        except OllamaNoDisponibleError as error:
            print(f"\n[Error] {error}")


if __name__ == "__main__":
    main()
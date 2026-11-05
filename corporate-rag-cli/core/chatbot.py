"""Logica del chatbot: consulta -> retrieval -> generacion -> respuesta."""

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from core.rag_system import RAGSystem

SYSTEM_PROMPT = (
    "Eres el asistente interno de la empresa. Responde en español, de forma "
    "clara y concisa, usando UNICAMENTE la informacion del contexto recuperado "
    "de los documentos internos. Si la respuesta no esta en el contexto, di que "
    "no dispones de esa informacion en los documentos, sin inventar nada."
)

class Chatbot:
    """Chatbot conversacional que integra el sistema RAG."""

    def __init__(self, rag_system: RAGSystem, model: str = "gpt-4o") -> None:
        self.rag = rag_system
        # Usamos gpt-4o por defecto ya que es el estándar actual más eficiente y capaz
        self.llm = ChatOpenAI(model=model)
        self._history: list = []

    def ask(self, question: str) -> str:
        """Responde a la pregunta usando RAG y conserva el contexto."""
        
        # 1. Recupera el contexto relevante del Vector Store
        context = self.rag.retrieve_context(question)
        
        # 2. Construye la lista de mensajes
        messages = [SystemMessage(content=SYSTEM_PROMPT)]
        
        # Añadir el historial de la conversación previa
        if self._history:
            messages.extend(self._history)
            
        # Preparar el mensaje actual inyectando el contexto y la pregunta
        current_prompt = (
            f"Contexto recuperado de los documentos internos:\n{context}\n\n"
            f"Pregunta del usuario: {question}"
        )
        messages.append(HumanMessage(content=current_prompt))
        
        # 3. Invoca el modelo y extrae el texto
        response = self.llm.invoke(messages)
        answer = response.content
        
        # 4. Guarda la interacción en el historial
        # Nota arquitectónica: Solo guardamos la pregunta original (sin el contexto inyectado) 
        # para no saturar la ventana de contexto del LLM en turnos futuros.
        self._history.append(HumanMessage(content=question))
        self._history.append(AIMessage(content=answer))
        
        # 5. Devuelve la respuesta final
        return answer
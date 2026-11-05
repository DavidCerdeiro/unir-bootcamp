"""Sistema RAG: carga de documentos, embeddings, vector store y retrieval."""

from pathlib import Path

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class RAGSystem:
    """Gestiona los embeddings y la recuperación de fragmentos relevantes."""

    def __init__(self, documents_dir: str = "documents") -> None:
        self.documents_dir = Path(documents_dir)
        
        # Inicialización del modelo de embeddings y el Vector Store en memoria
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.vector_store = InMemoryVectorStore(embedding=self.embeddings)
        
        # Configuración del text splitter optimizado para markdown/texto
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=120,
            separators=["\n\n", "\n", " ", ""]
        )

    def load_documents(self) -> int:
        """Carga, trocea y vectoriza los documentos markdown."""
        
        if not self.documents_dir.exists() or not self.documents_dir.is_dir():
            raise FileNotFoundError(f"El directorio {self.documents_dir} no existe.")

        md_files = list(self.documents_dir.glob("*.md"))
        
        if not md_files:
            raise FileNotFoundError(f"No se encontraron archivos .md en el directorio {self.documents_dir}.")

        documents = []
        for file_path in md_files:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                # Crear el Document de langchain guardando el nombre del archivo en la metadata
                doc = Document(
                    page_content=content, 
                    metadata={"source": file_path.name}
                )
                documents.append(doc)

        # Trocear los documentos en fragmentos más pequeños
        chunks = self.splitter.split_documents(documents)
        
        # Añadir los fragmentos al vector store
        self.vector_store.add_documents(chunks)
        
        return len(chunks)

    def retrieve(self, query: str, k: int = 4) -> list[Document]:
        """Devuelve los k fragmentos más relevantes para la consulta."""
        # Búsqueda por similitud delegada al vector store
        return self.vector_store.similarity_search(query, k=k)

    def retrieve_context(self, query: str, k: int = 4) -> str:
        """Devuelve los fragmentos relevantes formateados para el prompt."""
        docs = self.retrieve(query, k=k)
        
        if not docs:
            return "No se encontró información relevante en los documentos."

        # Formatear cada fragmento indicando su origen
        context_parts = []
        for i, doc in enumerate(docs, start=1):
            source = doc.metadata.get("source", "Documento desconocido")
            context_parts.append(f"--- Fragmento {i} (Fuente: {source}) ---\n{doc.page_content}\n")
            
        return "\n".join(context_parts)
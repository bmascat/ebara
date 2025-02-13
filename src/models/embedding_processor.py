import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingProcessor:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embedding_model)
        self.index = faiss.IndexFlatL2(self.embedder.get_sentence_embedding_dimension())
        self.docs = []
    
    def chunk_and_embed(self, documents: list, chunk_size=512):
        """Realiza chunking y embedding de los artículos."""
        chunks = [documents[i:i+chunk_size] for i in range(0, len(documents), chunk_size)]
        self.docs.extend(chunks)
        embeddings = self.embedder.encode(chunks)
        self.index.add(np.array(embeddings, dtype=np.float32))
   
    def process_abstracts(self, abstracts: list):
        """
        Procesa una lista de abstracts, calcula sus embeddings y los añade al índice FAISS.
        
        Args:
            abstracts: Lista de strings conteniendo los abstracts a procesar
        """
        if not abstracts:
            return
            
        # Calcular embeddings de todos los abstracts
        embeddings = self.embedder.encode(abstracts, convert_to_numpy=True)
        embeddings = np.array(embeddings, dtype=np.float32)
        
        # Añadir los abstracts y sus embeddings
        self.docs.extend(abstracts)
        self.index.add(embeddings)
    
    def retrieve_relevant_docs(self, query: str, top_k=5):
        """Encuentra los fragmentos más relevantes en FAISS."""
        query_embedding = self.embedder.encode([query])
        _, indices = self.index.search(np.array(query_embedding, dtype=np.float32), top_k)
        return [self.docs[idx] for idx in indices[0]]
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingProcessor:
    def __init__(self, embedding_model="all-MiniLM-L6-v2"):
        self.embedder = SentenceTransformer(embedding_model)
        self.index = faiss.IndexFlatL2(self.embedder.get_sentence_embedding_dimension())
        self.docs = []
    
    def chunk_and_embed(self, documents: list, chunk_size=512):
        """Performs chunking and embedding of the articles."""
        chunks = [documents[i:i+chunk_size] for i in range(0, len(documents), chunk_size)]
        self.docs.extend(chunks)
        embeddings = self.embedder.encode(chunks)
        self.index.add(np.array(embeddings, dtype=np.float32))
   
    def process_abstracts(self, abstracts: list):
        """
        Processes a list of abstracts, calculates their embeddings and adds them to the FAISS index.
        
        Args:
            abstracts: List of strings containing the abstracts to process
        """
        if not abstracts:
            return
            
        # Calculate embeddings of all abstracts
        embeddings = self.embedder.encode(abstracts, convert_to_numpy=True)
        embeddings = np.array(embeddings, dtype=np.float32)
        
        # Add the abstracts and their embeddings
        self.docs.extend(abstracts)
        self.index.add(embeddings)
    
    def retrieve_relevant_docs(self, query: str, top_k=5):
        """Finds the most relevant fragments in FAISS."""
        query_embedding = self.embedder.encode([query])
        _, indices = self.index.search(np.array(query_embedding, dtype=np.float32), top_k)
        return [self.docs[idx] for idx in indices[0]]
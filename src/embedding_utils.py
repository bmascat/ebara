# embedding_utils.py

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from sample_data import articles

# Cargamos el modelo de embeddings (puedes cambiarlo si lo deseas)
model = SentenceTransformer('all-MiniLM-L6-v2')
dimension = 384  # Dimensión de los embeddings para el modelo utilizado

# Inicializamos el índice FAISS y la lista de artículos
index = faiss.IndexFlatL2(dimension)
articles_list = articles  # Lista de artículos a indexar

def initialize_index():
    """
    Calcula los embeddings de los abstracts de los artículos y construye el índice FAISS.
    """
    texts = [article["abstract"] for article in articles_list]
    embeddings = model.encode(texts, convert_to_numpy=True).astype("float32")
    index.add(embeddings)

# Se inicializa el índice al importar el módulo
initialize_index()

def compute_embedding(text: str) -> np.ndarray:
    """
    Calcula el embedding de un texto dado.
    """
    embedding = model.encode([text], convert_to_numpy=True).astype("float32")
    return embedding[0]

def search_vector_db(query_embedding: np.ndarray, top_k: int = 3):
    """
    Busca en el índice FAISS los artículos más similares al embedding de la consulta.
    """
    query_embedding = np.array([query_embedding])
    distances, indices = index.search(query_embedding, top_k)
    results = []
    for idx in indices[0]:
        if idx < len(articles_list):
            results.append(articles_list[idx])
    return results

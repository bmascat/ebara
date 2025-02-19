from pymed import PubMed
from .base_retriever import BaseRetriever
from typing import List

class PubMedRetriever(BaseRetriever):
    """
    Retriever para la base de datos PubMed.
    Utiliza PyMed para conectarse a la API de PubMed.
    """

    def __init__(self, max_results: int = 20):
        super().__init__(max_results)
        self.pubmed = PubMed()

    def fetch_articles(self, query: str) -> List[str]:
        """
        Obtiene los primeros 'max_results' artículos de PubMed según la consulta.
        
        Args:
            query (str): Query de búsqueda
            
        Returns:
            List[str]: Lista de abstracts de los artículos
        """
        results = self.pubmed.query(query, max_results=self.max_results)
        abstracts = []
        for article in results:
            if article.abstract:
                abstracts.append(article.abstract)
        return abstracts

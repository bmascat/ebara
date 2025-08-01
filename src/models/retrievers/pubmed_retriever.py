from pymed import PubMed
from .base_retriever import BaseRetriever
from typing import List

class PubMedRetriever(BaseRetriever):
    """
    PubMedRetriever for the PubMed database.
    Uses PyMed to connect to the PubMed API.
    """

    def __init__(self, max_results: int = 15):
        super().__init__(max_results)
        self.pubmed = PubMed()

    def fetch_articles(self, query: str) -> List[str]:
        """
        Obtains the first 'max_results' articles from PubMed according to the query.
        
        Args:
            query (str): search query
            
        Returns:
            List[dict]: List of objects containing doi, title, and abstract of the articles
        """
        results = self.pubmed.query(query, max_results=self.max_results)
        articles = []
        for article in results:
            if article.abstract:
                articles.append({
                    'doi': article.doi,
                    'title': article.title,
                    'abstract': article.abstract
                })
        return articles

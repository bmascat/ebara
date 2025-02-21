import requests
from typing import List
from .base_retriever import BaseRetriever

class EuropePMCRetriever(BaseRetriever):
    """
    Retriever for the Europe PMC database.
    Uses the Europe PMC REST API.
    """

    BASE_URL = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"

    def __init__(self, max_results: int = 20):
        super().__init__(max_results)

    def fetch_articles(self, query: str) -> List[str]:
        """
        Obtains the first 'max_results' articles from Europe PMC according to the query.
        
        Args:
            query (str): Search query
            
        Returns:
            List[str]: List of abstracts of the articles
        """
        params = {
            'query': query,
            'format': 'json',
            'pageSize': self.max_results
        }
        
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        titles = [] 
        
        for result in data.get('resultList', {}).get('result', []):
            if 'title' in result:
                titles.append(result['title'])
                
        return titles

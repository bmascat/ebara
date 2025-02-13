from pymed import PubMed

class PubMedRetriever:
    """
    Clase para manejar la consulta a PubMed y obtener los artículos relevantes.
    Utiliza PyMed para conectarse a la API de PubMed.
    """

    def __init__(self, max_results=20):
        self.pubmed = PubMed()
        self.max_results = max_results

    def fetch_articles(self, query: str) -> list:
        """
        Obtiene los primeros 'max_results' artículos de PMC según la consulta.
        Devuelve una lista de abstracts de los artículos.
        """
        results = self.pubmed.query(query, max_results=self.max_results)
        abstracts = []
        for article in results:
            if article.abstract:
                abstracts.append(article.abstract)
        return abstracts

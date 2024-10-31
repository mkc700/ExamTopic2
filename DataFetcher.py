import requests

class DataFetcher:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        """Obtiene datos de la API y los retorna como una lista de diccionarios."""
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Verificar si hubo errores en la solicitud
            return response.json()  # Devolver los datos como objeto JSON
        except requests.RequestException as e:
            print(f"Error al obtener datos: {e}")
            return []  # Retorna una lista vacía en caso de error

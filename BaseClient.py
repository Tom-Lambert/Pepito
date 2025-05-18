import requests

class BaseClient:
    def __init__(self, base_url: str, headers: dict = {}):
        self.base_url = base_url.rstrip('/')  # Nettoyage de l'URL de base
        self.headers = headers

    def http_request(self, method: str, endpoint: str, json_body: dict = {}, headers: dict = {}, verify_ssl: bool = True):
        url = f"{self.base_url}/{endpoint.lstrip('/')}"  # Construire l'URL complète
        all_headers = {**self.headers, **headers}  # Fusion des en-têtes

        response = requests.request(
            method=method.upper(),
            url=url,
            headers=all_headers,
            json=json_body if method.upper() in ["POST", "PUT"] else None,
            verify=verify_ssl
        )

        response.raise_for_status() 
        return response.json()  # Retourne la réponse JSON

from BaseClient import BaseClient

class AbuseIPDBClient(BaseClient):
    def __init__(self, base_url: str, api_key: str):
        headers = {
            "Key": api_key,
            "Accept": "application/json"
        }
        super().__init__(base_url, headers)

    def check_reputation(self, ip: str = None, domain: str = None):
        if not ip:
            raise ValueError("IP address is required for AbuseIPDB reputation check.")
        
        # On construit l'URL de l'API
        endpoint = f"api/v2/check?ipAddress={ip}&maxAgeInDays=90"
        return self.http_request("GET", endpoint)

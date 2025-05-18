import certstream
import json
import socket
from AbuseIPDBClient import AbuseIPDBClient
from Logger import Logger
from Api import API_KEY


with open("domain.json", "r") as f:
    KEYWORDS = json.load(f)

# Configuration de l'API AbuseIPDB
abuse_client = AbuseIPDBClient("https://api.abuseipdb.com", API_KEY)

# Option pour le print 
logger = Logger(print_logs=True)

def my_callback(message, context):

    # On ne traite que les messages de type "certificate_update"
    if message["message_type"] != "certificate_update":
        return


    cert_data = message["data"]

    # Récupération des domaines
    all_domains = cert_data.get("leaf_cert", {}).get("all_domains", [])

    # Récupération emmeteur 
    issuer = cert_data.get("chain", [{}])[0].get("subject", "Unknown")
    suspicious_domains = []

    # On ne traite que les domaines qui contiennent des mots-clés
    for domain in set(all_domains):
        match_score = 0
        for keyword, weight in KEYWORDS.items():
            if keyword in domain:
                match_score = weight
                break

        if match_score == 0:
            continue 
        
        # Appel à l'API AbuseIPDB pour vérifier la réputation de l'IP
        try:
            ip = socket.gethostbyname(domain)
            rep_data = abuse_client.check_reputation(ip)
            abuse_score = rep_data.get("data", {}).get("abuseConfidenceScore", 0)
        except Exception:
            abuse_score = 0

        issuer_penalty = 20 if "Let's Encrypt" in issuer else 0
        suspicion_score = match_score + abuse_score + issuer_penalty

        if suspicion_score > 80:
            level = "[HIGH]"
        elif suspicion_score > 50:
            level = "[MEDIUM]"
        else:
            level = "[LOW]"

        if suspicion_score >= 50:
            suspicious_domains.append(f"{domain}({match_score})")

    if suspicious_domains:
        logger.alert(f"{level} {','.join(suspicious_domains)} ({issuer})")

def on_open():
    print("[*] Connexion établie avec certstream-server-go.")

def on_error(instance, exception):
    print("[!] Erreur dans le client CertStream :", exception)

def main():
    print("[*] Connexion à ws://127.0.0.1:8080/full")
    certstream.listen_for_events(
        my_callback,
        on_open=on_open,
        on_error=on_error,
        url='ws://127.0.0.1:8080/full'  # ← Connexion locale au serveur Go
    )

if __name__ == "__main__":
    main()

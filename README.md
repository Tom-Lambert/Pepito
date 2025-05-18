# Project PEPITO

Ce projet utilise un serveur local `certstream-go-server` pour écouter les certificats SSL en temps réel, combiné à un script Python exploitant une clé API externe.
Ce n'est pas une version Pepito afin de voir plus facilement les différents certificats SSL.

---

## Prérequis

- Serveur local : [`certstream-server-go`](https://github.com/CaliDog/certstream-server-go)
- Python 3
- Une clé API valide

---

## Configuration du serveur `certstream-go-server`

Exemple de fichier de configuration (`config.yaml`) :

```yaml
log-level: "info"

webserver:
  listen_addr: "127.0.0.1"
  listen_port: 8080
  full_url: "/full"
  lite_url: "/lite"
  domains_only_url: "/domains"
  compression_enabled: false

prometheus:
  listen_addr: "127.0.0.1"
  listen_port: 9100
  enabled: false
  metrics_url: "/metrics"
  expose_system_metrics: false

general:
  additional_logs: []
  buffer_sizes:
    websocket: 300
    ctlog: 1000
    broadcastmanager: 10000
  drop_old_logs: true
```

---

## Ajouter votre clé API

Créer le fichier `API.py` et mettre la valeur de `API_KEY` par ta clé personnelle :

```python
API_KEY = "YOUR_API_KEY"
```

---

## Lancer le script

Une fois le serveur lancé et la clé API renseignée, exécute simplement :

```bash
python3 ./main.py
```

---

## Remarques

- Le script communique uniquement avec le serveur local (`127.0.0.1:8080`).
- Le port 8080 doit être libre.

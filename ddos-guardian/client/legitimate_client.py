import os, time
import requests

URL = os.getenv("TARGET_URL", "http://localhost:8000/health")

while True:
    try:
        resposta = requests.get(URL, timeout=2)
        print("[CLIENTE]", resposta.status_code)
    except requests.RequestException as erro:
        print("Erro na requisição:", erro)
    time.sleep(1) 
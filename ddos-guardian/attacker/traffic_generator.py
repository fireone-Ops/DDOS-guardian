import os

import requests

URL = os.getenv("TARGET_URL", "http://localhost:8000/health")

contagem = {}                   
bloqueado_na = None             

for i in range(1, 1001):
    try:
        resposta = requests.get(URL, timeout=2)
        status = resposta.status_code
    except requests.RequestException:
        status = "erro"       
    contagem[status] = contagem.get(status, 0) + 1
    if status == 429 and bloqueado_na is None:
        bloqueado_na = i
        print("[ATACANTE] Requisição bloqueada na posição:", bloqueado_na)

print(contagem)
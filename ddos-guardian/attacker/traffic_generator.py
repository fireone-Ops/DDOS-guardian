import os, time

import requests # type: ignore


URL = os.getenv("TARGET_URL", "http://localhost:8000/health")

ATRASO = float(os.getenv("ATRASO", "0"))
TOTAL = int(os.getenv("TOTAL", "1000"))

contagem = {}                   
bloqueado_na = None             

for i in range(1, TOTAL + 1):
    time.sleep(ATRASO)
    try:
        resposta = requests.get(URL, timeout=2)
        status = resposta.status_code
    except requests.RequestException:
        status = "erro"       
    contagem[status] = contagem.get(status, 0) + 1
    if status == 429 and bloqueado_na is None:
        bloqueado_na = i
        print("[ATACANTE] Requisição bloqueada na posição:", bloqueado_na)
    time.sleep(ATRASO)

print(contagem)
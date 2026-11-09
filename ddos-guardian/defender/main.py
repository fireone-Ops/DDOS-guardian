import time
from collections import defaultdict, deque
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

LIMITE = 100
JANELA = 10
LIMITE_EMERGENCIA = 20
LIMITE_GLOBAL = 200

historico = defaultdict(deque)
historico_global = deque()

def modo_emergencia(agora):
    historico_global.append(agora)
    while historico_global and agora - historico_global[0] > JANELA:
        historico_global.popleft()
    return len(historico_global) > LIMITE_GLOBAL

def registrar(ip):
    agora = time.time()
    emergencia = modo_emergencia(agora)
    limite = LIMITE_EMERGENCIA if emergencia else LIMITE
    historico[ip].append(agora)
    while historico[ip] and agora - historico[ip][0] > JANELA:
        historico[ip].popleft()

    return len(historico[ip]) > limite

@app.get("/health")
def health(request: Request):
    ip = request.headers.get("x-real-ip") or request.client.host
    if registrar(ip):
        raise HTTPException(status_code=429, detail="Too many requests")
    return {"status": "ok"}
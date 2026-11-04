import time
from collections import defaultdict, deque
from fastapi import FastAPI, HTTPException, Request

app = FastAPI()

LIMITE = 100
JANELA = 10

historico = defaultdict(deque)

def registrar(ip):
    agora = time.time()
    historico[ip].append(agora)
    while historico[ip] and agora - historico[ip][0] > JANELA:
        historico[ip].popleft()

    return len(historico[ip]) > LIMITE

@app.get("/health")
def health(request: Request):
    ip = request.headers.get("x-real-ip") or request.client.host
    if registrar(ip):
        raise HTTPException(status_code=429, detail="Too many requests")
    return {"status": "ok"}

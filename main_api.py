from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import threading
import time
from datetime import datetime
import os
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

SYMBOL = os.getenv("SYMBOL", "ITUB4")
LOOP_SECONDS = int(os.getenv("LOOP_SECONDS", "60"))
INITIAL_BALANCE = float(os.getenv("INITIAL_BALANCE", "50"))
PAPER_TRADING = os.getenv("PAPER_TRADING", "true").lower() == "true"

estado = {
    "status": "iniciando",
    "ativo": SYMBOL,
    "ultimo_preco": None,
    "ultimo_sinal": "nenhum",
    "tipo_sinal": "nenhum",
    "horario": None,
    "saldo_paper": INITIAL_BALANCE,
    "operacoes": 0,
    "logs": []
}

def registrar_log(msg: str):
    horario = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"[{horario}] {msg}"
    estado["logs"].insert(0, linha)
    estado["logs"] = estado["logs"][:20]
    print(linha)

def executar_analise():
    preco = round(random.uniform(30, 40), 2)

    if preco < 33:
        sinal = "possível entrada"
        tipo = "compra"
    elif preco > 37:
        sinal = "entrada garantida"
        tipo = "compra"
    else:
        sinal = "aguardando"
        tipo = "neutro"

    estado["status"] = "rodando"
    estado["ultimo_preco"] = preco
    estado["ultimo_sinal"] = sinal
    estado["tipo_sinal"] = tipo
    estado["horario"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    if PAPER_TRADING and tipo == "compra":
        estado["operacoes"] += 1

    registrar_log(f"Análise concluída em {SYMBOL} | preço={preco} | sinal={sinal}")

def loop_vaiiixbr():
    while True:
        try:
            executar_analise()
        except Exception as e:
            estado["status"] = "erro"
            registrar_log(f"Erro na execução: {e}")
        time.sleep(LOOP_SECONDS)

@app.on_event("startup")
def startup_event():
    thread = threading.Thread(target=loop_vaiiixbr, daemon=True)
    thread.start()
    registrar_log("Loop automático da VAIIIxBR iniciado")

@app.get("/")
def root():
    return {"message": "VAIIIxBR online"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    return estado

@app.get("/signal")
def signal():
    return {
        "ativo": estado["ativo"],
        "ultimo_preco": estado["ultimo_preco"],
        "ultimo_sinal": estado["ultimo_sinal"],
        "tipo_sinal": estado["tipo_sinal"],
        "horario": estado["horario"]
    }

@app.get("/metrics")
def metrics():
    return {
        "saldo_paper": estado["saldo_paper"],
        "operacoes": estado["operacoes"],
        "status": estado["status"]
    }

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "estado": estado
    })

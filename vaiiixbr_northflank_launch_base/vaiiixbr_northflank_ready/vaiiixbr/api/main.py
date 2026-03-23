from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from vaiiixbr.config import Settings
from vaiiixbr.storage.repository import Repository
from vaiiixbr.storage.sqlite_store import SQLiteStore

settings = Settings()
store = SQLiteStore(settings)
repository = Repository(store)
app = FastAPI(title="VAIIIxBR API", version="1.0.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/status")
def status() -> dict:
    return repository.get_status()


@app.get("/signals")
def signals(limit: int = 20) -> list[dict]:
    return repository.list_signals(limit=limit)


@app.get("/paper-trades")
def paper_trades(limit: int = 20) -> list[dict]:
    return repository.list_paper_trades(limit=limit)


@app.get("/", response_class=HTMLResponse)
def dashboard() -> str:
    status = repository.get_status()
    signal = status.get("signal", {})
    paper = status.get("paper", {})
    metrics = status.get("metrics", {}).get("trades", {})
    return f"""
    <!doctype html>
    <html>
      <head>
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <title>VAIIIxBR</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 20px; background:#0f172a; color:#e2e8f0; }}
          .card {{ background:#1e293b; border-radius:16px; padding:16px; margin-bottom:12px; }}
          .muted {{ color:#94a3b8; }}
          .value {{ font-size:24px; font-weight:700; }}
        </style>
      </head>
      <body>
        <div class='card'><div class='muted'>Ativo</div><div class='value'>{status.get('asset','ITUB4')}</div></div>
        <div class='card'><div class='muted'>Decisão</div><div class='value'>{signal.get('decision','neutro')}</div></div>
        <div class='card'><div class='muted'>Score</div><div class='value'>{signal.get('long_score','-')}</div></div>
        <div class='card'><div class='muted'>Modo</div><div class='value'>{signal.get('pre_analysis_mode','normal')}</div></div>
        <div class='card'><div class='muted'>Paper Cash / Equity</div><div class='value'>R$ {paper.get('cash','-')} / R$ {paper.get('equity','-')}</div></div>
        <div class='card'><div class='muted'>Win rate</div><div class='value'>{round(float(metrics.get('win_rate',0.0)),2)}%</div></div>
        <div class='card'><div class='muted'>Atualizado em</div><div>{status.get('updated_at','sem dados')}</div></div>
      </body>
    </html>
    """

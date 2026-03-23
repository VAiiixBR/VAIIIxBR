# VAIIIxBR Northflank Base

Versão revisada e preparada para nuvem da VAIIIxBR.

## O que mudou
- troca de CSV solto por **SQLite** para sinais, trades e status atual;
- separação clara entre **worker** e **API/dashboard**;
- foco em uso em nuvem com **Northflank** como base;
- retirada da dependência de **Tkinter** para ambiente cloud;
- dashboard web responsivo para abrir em qualquer celular;
- estrutura pronta para evoluir com notificadores externos e autenticação.

## Arquitetura
- `main_worker.py`: loop contínuo da VAIIIxBR
- `main_api.py`: API FastAPI + dashboard
- `vaiiixbr/services.py`: orquestra o motor da IA
- `vaiiixbr/storage/`: persistência em SQLite
- `vaiiixbr/strategy/`: pré-análise e pipeline
- `vaiiixbr/execution/paper_trader.py`: paper trading com caixa inicial de R$50

## Rodando localmente
```bash
pip install -r requirements.txt
python main_worker.py
uvicorn main_api:app --reload
```

## Variáveis importantes
- `BRAPI_TOKEN`
- `PORT`
- `VAIII_POLL_SECONDS`
- `VAIII_PAPER_INITIAL_CASH`

## Deploy na Northflank
Crie **dois serviços** usando o mesmo repositório/imagem:

1. **API Web**
   - Start command:
   ```bash
   uvicorn main_api:app --host 0.0.0.0 --port $PORT
   ```

2. **Worker**
   - Start command:
   ```bash
   python main_worker.py
   ```

Monte um volume persistente em `/app/data` para manter o SQLite.

## Endpoints
- `/health`
- `/status`
- `/signals`
- `/paper-trades`
- `/` dashboard web

## Falhas iniciais removidas
- sinal repetido no mesmo candle sem trava adequada;
- persistência frágil em CSV para ambiente cloud;
- notificação desktop incompatível com nuvem;
- acoplamento excessivo entre loop, UI e armazenamento;
- falta de API web para acesso por celular.


## Arquivos adicionados para Northflank
- `northflank/runtime.env.example`: variáveis-base
- `northflank/service-commands.txt`: comandos do web e worker
- `northflank/DEPLOY_NORTHFLANK.md`: passo a passo de deploy
- `northflank/northflank.base.yaml`: mapa-base de configuração
- `.dockerignore`: limpeza de build

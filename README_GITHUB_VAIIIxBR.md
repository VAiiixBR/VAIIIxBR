# VAIIIxBR — Arquivo para subir o projeto no GitHub

## Objetivo
Este arquivo serve como guia prático para publicar o projeto **VAIIIxBR** no GitHub e deixar o repositório pronto para deploy no Northflank.

---

## Estrutura recomendada do projeto

```text
VAIIIxBR/
  Dockerfile
  requirements.txt
  main_api.py
  templates/
    dashboard.html
  README.md
```

---

## Arquivos mínimos esperados

### `main_api.py`
Arquivo principal da API FastAPI e do loop interno da VAIIIxBR.

### `requirements.txt`
Lista de dependências Python.

Exemplo:
```txt
fastapi
uvicorn
jinja2
requests
pandas
numpy
```

### `Dockerfile`
Arquivo que o Northflank vai usar para buildar e subir a aplicação.

Exemplo:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn main_api:app --host 0.0.0.0 --port ${PORT:-8000}"]
```

---

## Como subir a VAIIIxBR no GitHub

### Opção 1 — Pelo computador usando Git
Use essa opção se você tem a pasta do projeto no seu PC.

Abra o terminal dentro da pasta do projeto e execute:

```bash
git init
git add .
git commit -m "Primeira versao VAIIIxBR"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/VAIIIxBR.git
git push -u origin main
```

Depois disso, o projeto estará publicado no GitHub.

---

### Opção 2 — Criando o repositório primeiro no GitHub
1. Entre no GitHub.
2. Clique em **New repository**.
3. Dê o nome **VAIIIxBR**.
4. Crie o repositório vazio.
5. Copie a URL do repositório.
6. No terminal da pasta do projeto, rode:

```bash
git init
git add .
git commit -m "Primeira versao VAIIIxBR"
git branch -M main
git remote add origin URL_DO_REPOSITORIO
git push -u origin main
```

Substitua `URL_DO_REPOSITORIO` pela URL copiada do GitHub.

---

### Opção 3 — Upload manual pelo site do GitHub
Use essa opção se você ainda não quer usar terminal.

1. Crie um repositório novo no GitHub.
2. Abra o repositório.
3. Clique em **Add file**.
4. Clique em **Upload files**.
5. Arraste os arquivos do projeto.
6. Clique em **Commit changes**.

Essa opção funciona, mas é pior para manter o projeto, porque cada alteração precisa ser enviada manualmente.

---

## Melhor opção para a VAIIIxBR
A melhor opção é a **Opção 1 ou 2 com Git pelo terminal**.

Motivos:
- mais profissional
- mais rápida
- facilita deploy automático no Northflank
- cada atualização do projeto vira um commit
- dá para integrar com branch principal e redeploy automático

---

## Como atualizar o projeto depois
Sempre que você alterar algo no código, rode:

```bash
git add .
git commit -m "Atualizacao da VAIIIxBR"
git push
```

Isso envia a nova versão para o GitHub.

---

## Como conectar ao Northflank depois
Depois que o projeto estiver no GitHub:

1. Abra o Northflank.
2. Crie ou abra seu projeto.
3. Crie um serviço novo.
4. Escolha deploy via repositório Git.
5. Conecte sua conta GitHub.
6. Selecione o repositório **VAIIIxBR**.
7. Escolha a branch `main`.
8. Use o `Dockerfile` da raiz.
9. Faça o deploy.

---

## Variáveis de ambiente recomendadas
No Northflank, configure:

```env
SYMBOL=ITUB4
LOOP_SECONDS=60
INITIAL_BALANCE=50
PAPER_TRADING=true
```

---

## Testes após o deploy
Com o serviço online, teste:

```text
/
 /health
 /status
 /dashboard
```

Resultados esperados:
- `/` retorna mensagem da API
- `/health` retorna status ok
- `/status` mostra o estado da IA
- `/dashboard` abre a página visual no celular

---

## Resumo prático
Para subir a VAIIIxBR corretamente:

1. organizar a pasta do projeto
2. criar repositório no GitHub
3. enviar os arquivos com Git
4. conectar o repositório ao Northflank
5. fazer o deploy com Dockerfile
6. testar as rotas da API

---

## Recomendação final
Para a VAIIIxBR, use sempre este fluxo:

**Projeto local -> GitHub -> Northflank**

Esse é o caminho mais estável para continuar evoluindo a IA.

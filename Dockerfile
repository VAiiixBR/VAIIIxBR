FROM python:3.11-slim

<<<<<<< HEAD
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/data
EXPOSE 8000

CMD ["sh", "-c", "uvicorn main_api:app --host 0.0.0.0 --port ${PORT:-8000}"]
=======
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["sh", "-c", "python -m uvicorn main_api:app --host 0.0.0.0 --port ${PORT:-8000}"]
>>>>>>> ac67b77259844e6db039f70b66c94c290e235dec

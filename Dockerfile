# Use Python 3.12 slim
FROM python:3.12-slim

# Diretório de trabalho
WORKDIR /app

# Copiar requirements primeiro (cache de layers)
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código
COPY . .

# Expor porta 8080 (padrão do Fly.io)
EXPOSE 8080

# Comando para rodar o app
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]

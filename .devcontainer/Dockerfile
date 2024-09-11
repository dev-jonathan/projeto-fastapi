FROM python:3.11-slim

RUN mkdir /workspace
WORKDIR /workspace

# Instale dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
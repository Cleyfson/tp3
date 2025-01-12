# Use a imagem base oficial do Python
FROM python:3.10-slim

# Instala dependências do sistema
RUN apt-get update && apt-get install -y \
    redis-tools \
    && rm -rf /var/lib/apt/lists/*

# Define o diretório de trabalho no container
WORKDIR /app

# Copia o código da aplicação para o container
COPY dashboard.py .

# Instala as dependências do Python
RUN pip install --no-cache-dir streamlit redis

# Expondo a porta 8501 para o Streamlit
EXPOSE 8501

# Comando para rodar o Streamlit
CMD ["streamlit", "run", "dashboard.py", "--server.port", "8501", "--server.enableCORS", "false"]

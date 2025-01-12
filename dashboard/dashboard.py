import streamlit as st
import redis
import json
import time

# Configurações do Redis
REDIS_HOST = "localhost"  # O endereço do seu Redis
REDIS_PORT = 6379
REDIS_KEY = "metrics-output"  # Chave do Redis onde os dados serão armazenados

# Função para conectar ao Redis
def connect_to_redis():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

# Função para ler dados do Redis
def get_data_from_redis(redis_client):
    try:
        data = redis_client.get(REDIS_KEY)
        if data:
            return json.loads(data)
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao ler do Redis: {e}")
        return None

# Função para exibir os dados no Streamlit
def display_metrics(data):
    if data:
        st.write("### Métricas de Sistema")
        st.write(f"**Percentual de Egressos de Rede**: {data.get('percent-network-egress', 'N/A')}%")
        st.write(f"**Percentual de Cache de Memória**: {data.get('percent-memory-cache', 'N/A')}%")
        
        for key, value in data.items():
            if key.startswith("avg-util-cpu"):
                st.write(f"{key}: {value}%")
    else:
        st.write("Nenhum dado disponível.")

# Função principal para a interface do dashboard
def main():
    st.title("Dashboard de Monitoramento de Sistema")

    # Conecta ao Redis
    redis_client = connect_to_redis()

    while True:
        # Lê os dados do Redis
        data = get_data_from_redis(redis_client)

        # Exibe as métricas
        display_metrics(data)

        # Atualiza a cada 5 segundos
        time.sleep(5)
        st.experimental_rerun()

if __name__ == "__main__":
    main()

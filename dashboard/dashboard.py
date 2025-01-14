import streamlit as st
import redis
import json
import os
import time


def connect_redis():
    """Conecta ao Redis usando variáveis de ambiente."""
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = int(os.getenv('REDIS_PORT', 6379))
    return redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)


def fetch_metrics(redis_client, key):
    """Busca métricas do Redis."""
    try:
        data = redis_client.get(key)
        if data:
            return json.loads(data)
        return {}
    except Exception as e:
        st.error(f"Erro ao buscar dados do Redis: {e}")
        return {}


def main():
    # Configuração do título
    st.title("Dashboard de Monitoramento")
    st.markdown("Exibe métricas computadas pelo servidor.")

    # Conectar ao Redis
    redis_client = connect_redis()
    redis_output_key = os.getenv("REDIS_OUTPUT_KEY", "metrics-output")

    # Exibição contínua
    st.sidebar.markdown("### Opções")
    refresh_rate = st.sidebar.slider("Taxa de atualização (segundos)", 1, 30, 5)

    st.header("Métricas")
    placeholder = st.empty()

    while True:
        metrics = fetch_metrics(redis_client, redis_output_key)

        with placeholder.container():
            if metrics:
                for metric, value in metrics.items():
                    st.metric(label=metric.capitalize(), value=value)
            else:
                st.warning("Nenhuma métrica encontrada no Redis.")

        time.sleep(refresh_rate)


if __name__ == "__main__":
    main()

import streamlit as st
import redis
import json


def get_redis_data(redis_host: str, redis_port: int, redis_key: str):
    client = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    data = client.get(redis_key)
    return json.loads(data) if data else {}


st.title("Monitoring Dashboard")
redis_host = st.text_input("Redis Host", "localhost")
redis_port = st.number_input("Redis Port", 6379)
redis_key = st.text_input("Redis Key", "2021040130-proj3-output")

if st.button("Load Data"):
    data = get_redis_data(redis_host, redis_port, redis_key)
    if data:
        st.json(data)
        st.line_chart({k: v for k, v in data.items() if k.startswith("avg-util-cpu")})
    else:
        st.error("No data found.")

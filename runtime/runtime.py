import os
import time
import redis
import json
import importlib.util
from typing import Any, Dict

class Context:
    def __init__(self):
        self.env = {}

    def update_env(self, new_env: Dict[str, Any]):
        self.env.update(new_env)

def load_function_from_config(pyfile_config: str):
    """
    Carrega o código da função handler a partir do ConfigMap
    """
    spec = importlib.util.spec_from_loader("handler", loader=None, origin="pyfile_config")
    handler_module = importlib.util.module_from_spec(spec)
    exec(pyfile_config, handler_module.__dict__)
    return handler_module.handler

def connect_redis():
    """
    Conecta ao Redis usando as variáveis de ambiente configuradas
    """
    redis_host = os.getenv('REDIS_HOST', 'localhost')
    redis_port = os.getenv('REDIS_PORT', 6379)
    return redis.StrictRedis(host=redis_host, port=redis_port, db=0)

def monitor_redis(redis_client, input_key: str, monitoring_period: int):
    """
    Monitora a chave do Redis periodicamente e retorna os dados quando houver atualização
    """
    last_value = None
    while True:
        data = redis_client.get(input_key)
        if data != last_value:
            last_value = data
            return json.loads(data)
        time.sleep(monitoring_period)

def main():
    # Carregar configuração do ConfigMap
    pyfile_config = os.getenv('PYFILE', '')  # Obtenha o código Python do ConfigMap
    redis_input_key = os.getenv('REDIS_INPUT_KEY', 'metrics-input')
    redis_output_key = os.getenv('REDIS_OUTPUT_KEY', 'metrics-output')
    redis_monitoring_period = int(os.getenv('REDIS_MONITORING_PERIOD', 5))
    function_entry_point = os.getenv('FUNCTION_ENTRY_POINT', 'handler')

    # Carregar o código Python e a função handler
    handler = load_function_from_config(pyfile_config)
    
    # Conectar ao Redis
    redis_client = connect_redis()

    # Criar contexto
    context = Context()

    while True:
        # Monitorar a chave do Redis para novos dados
        input_data = monitor_redis(redis_client, redis_input_key, redis_monitoring_period)

        # Chamar a função handler com os dados de entrada e o contexto
        result = handler(input_data, context)

        # Armazenar o resultado no Redis
        redis_client.set(redis_output_key, json.dumps(result))

if __name__ == '__main__':
    main()

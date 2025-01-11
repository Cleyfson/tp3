import redis
import json
from typing import Any, Dict


def handler(input: Dict[str, Any], context: Any) -> Dict[str, Any]:
    # Obtém a variável persistente do contexto
    env = context.env
    moving_averages = env.get("moving_averages", {})

    # Dados de entrada
    cpu_utilizations = [value for key, value in input.items() if key.startswith("cpu_percent-")]
    cached = input["virtual_memory-cached"]
    buffers = input["virtual_memory-buffers"]
    total_memory = input["virtual_memory-total"]
    bytes_sent = input["net_io_counters_eth0-bytes_sent1"]
    bytes_recv = input["net_io_counters_eth0-bytes_recv1"]

    # Calcula métricas
    percent_network_egress = bytes_sent / (bytes_sent + bytes_recv) * 100
    percent_memory_cache = (cached + buffers) / total_memory * 100

    # Calcula a média móvel por CPU
    for idx, utilization in enumerate(cpu_utilizations):
        key = f"avg-util-cpu{idx + 1}-60sec"
        if key in moving_averages:
            moving_averages[key] = (moving_averages[key] * 59 + utilization) / 60
        else:
            moving_averages[key] = utilization

    # Atualiza o contexto com as médias móveis
    env["moving_averages"] = moving_averages

    # Retorna os resultados
    result = {
        "percent-network-egress": percent_network_egress,
        "percent-memory-cache": percent_memory_cache,
        **moving_averages,
    }
    return result

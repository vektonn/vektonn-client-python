import socket
from contextlib import closing

from vektonn.dtos import Vector

vektonn_api_host = 'localhost'
vektonn_api_port = 8081
vektonn_api_base_url = f'http://{vektonn_api_host}:{vektonn_api_port}'

data_source_name = 'QuickStart.Source'
data_source_version = '1.0'

index_name = 'QuickStart.Index'
index_version = '1.0'

zero_vector = Vector(is_sparse=False, coordinates=[0.0, 0.0])


def _is_vektonn_running() -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((vektonn_api_host, vektonn_api_port)) == 0:
            return True
        else:
            return False


is_vektonn_running = _is_vektonn_running()

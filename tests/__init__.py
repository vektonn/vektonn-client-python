import socket
from contextlib import closing

from vektonn.dtos import VectorDto

vektonn_api_host = 'localhost'
vektonn_api_port = 8081
vektonn_api_base_url = f'http://{vektonn_api_host}:{vektonn_api_port}'

data_source_name = 'Samples.DenseVectors'
data_source_version = '0.1'

index_name = 'Samples.DenseVectors'
index_version = '0.1'

zero_vector = VectorDto(is_sparse=False, coordinates=[0.0, 0.0])


def _is_vektonn_running() -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((vektonn_api_host, vektonn_api_port)) == 0:
            return True
        else:
            return False


is_vektonn_running = _is_vektonn_running()

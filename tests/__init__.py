import socket
from contextlib import closing
from typing import List, Optional

from vektonn.dtos import Vector, Attribute, AttributeValue, InputDataPoint, FoundDataPoint

vektonn_api_host = 'localhost'
vektonn_api_port = 8081
vektonn_api_base_url = f'http://{vektonn_api_host}:{vektonn_api_port}'

data_source_name = 'QuickStart.Source'
data_source_version = '1.0'

index_name = 'QuickStart.Index'
index_version = '1.0'


def _is_vektonn_running() -> bool:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        if sock.connect_ex((vektonn_api_host, vektonn_api_port)) == 0:
            return True
        else:
            return False


is_vektonn_running = _is_vektonn_running()


def dense_vector(coordinates: List[float]) -> Vector:
    return Vector(is_sparse=False, coordinates=coordinates)


zero_vector = dense_vector(coordinates=[0.0, 0.0])


def int_attribute(key: str, value: int) -> Attribute:
    return Attribute(key=key, value=AttributeValue(int64=value))


def str_attribute(key: str, value: str) -> Attribute:
    return Attribute(key=key, value=AttributeValue(string=value))


def input_data_point(vector: List[float], dp_id: int, payload: str) -> InputDataPoint:
    return InputDataPoint(
        vector=dense_vector(coordinates=vector),
        attributes=[
            int_attribute(key='id', value=dp_id),
            str_attribute(key='payload', value=payload),
        ])


def found_data_point(vector: Optional[List[float]], dp_id: int, payload: str, distance: float) -> FoundDataPoint:
    return FoundDataPoint(
        vector=None if vector is None else dense_vector(coordinates=vector),
        attributes=[
            int_attribute(key='id', value=dp_id),
            str_attribute(key='payload', value=payload),
        ],
        distance=distance)

from datetime import datetime
from uuid import UUID

import pytest

from vektonn.dtos import (
    Attribute, AttributeValue, Vector, ErrorResult,
    UploadQuery, InputDataPoint, SearchResult, FoundDataPoint
)


def test_json_serialization__vector_dense():
    dto = Vector(
        is_sparse=False,
        coordinates=[1.0, 0, 0.1],
        coordinate_indices=None,
    )
    assert dto.json() == '{"isSparse":false,"coordinates":[1.0,0.0,0.1]}'


def test_json_serialization__vector_sparse():
    dto = Vector(
        is_sparse=True,
        coordinates=[1.0, 0.1],
        coordinate_indices=[7, 42],
    )
    assert dto.json() == '{"isSparse":true,"coordinates":[1.0,0.1],"coordinateIndices":[7,42]}'


@pytest.mark.parametrize(
    'dto, expected_json',
    [
        (Attribute(key='Str_Key', value=AttributeValue(string='Str_Value')),
         '{"key":"Str_Key","value":{"string":"Str_Value"}}'),
        (Attribute(key='UuidKey', value=AttributeValue(guid=UUID('12345678-1234-1234-1234-123456789abc'))),
         '{"key":"UuidKey","value":{"guid":"12345678-1234-1234-1234-123456789abc"}}'),
        (Attribute(key='bool_key', value=AttributeValue(bool=True)),
         '{"key":"bool_key","value":{"bool":true}}'),
        (Attribute(key='int_key', value=AttributeValue(int64=42)),
         '{"key":"int_key","value":{"int64":42}}'),
        (Attribute(key='int_key', value=AttributeValue(int64=0)),
         '{"key":"int_key","value":{"int64":0}}'),
        (Attribute(key='float_key', value=AttributeValue(float64=3.1415926)),
         '{"key":"float_key","value":{"float64":3.1415926}}'),
        (Attribute(
            key='DateTimeKey',
            value=AttributeValue(date_time=datetime(year=2021, month=11, day=23, hour=23, minute=59, second=1))),
         '{"key":"DateTimeKey","value":{"dateTime":"2021-11-23T23:59:01"}}'),
    ]
)
def test_json_serialization__attribute(dto: Attribute, expected_json: str):
    assert dto.json() == expected_json


def test_json_serialization__upload_query():
    dto = UploadQuery(__root__=[
        InputDataPoint(
            attributes=[(Attribute(key='k', value=AttributeValue(bool=False)))],
            vector=None,
            is_deleted=True,
        )
    ])
    assert dto.json() == '[{"attributes":[{"key":"k","value":{"bool":false}}],"isDeleted":true}]'


def test_json_deserialization__error():
    json = '{"errorMessages":["First error message","Second error message"]}'
    expected_dto = ErrorResult(error_messages=['First error message', 'Second error message'])
    assert ErrorResult.parse_raw(json) == expected_dto


def test_json_deserialization__search_result():
    json = '{' \
           '"queryVector":{"isSparse":false,"coordinates":[1,0,0.1]},' \
           '"nearestDataPoints":[' \
           '{"vector":{"isSparse":false,"coordinates":[1,0,0.1]},' \
           '"attributes":[{"key":"Id","value":{"int64":23}}],' \
           '"distance":0},' \
           '{"vector":{"isSparse":true,"coordinates":[-1,0,-0.1],"coordinateIndices":[7,0,42]},' \
           '"attributes":[{"key":"Id","value":{"int64":-1}},{"key":"Data","value":{"string":"some payload"}}],' \
           '"distance":0.2}' \
           ']' \
           '}'
    expected_dto = SearchResult(
        query_vector=Vector(is_sparse=False, coordinates=[1.0, 0.0, 0.1]),
        nearest_data_points=[
            FoundDataPoint(
                vector=Vector(is_sparse=False, coordinates=[1.0, 0.0, 0.1]),
                attributes=[Attribute(key="Id", value=AttributeValue(int64=23))],
                distance=0.0
            ),
            FoundDataPoint(
                vector=Vector(is_sparse=True, coordinates=[-1.0, 0.0, -0.1], coordinate_indices=[7, 0, 42]),
                attributes=[
                    Attribute(key="Id", value=AttributeValue(int64=-1)),
                    Attribute(key="Data", value=AttributeValue(string='some payload')),
                ],
                distance=0.2
            ),
        ]
    )
    assert SearchResult.parse_raw(json) == expected_dto

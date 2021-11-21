from datetime import datetime
from uuid import UUID

import pytest

from vektonn.dtos import (
    AttributeDto, AttributeValueDto, VectorDto, ErrorDto,
    UploadQueryDto, InputDataPointDto, SearchResultDto, FoundDataPointDto
)


def test_json_serialization__vector_dense():
    dto = VectorDto(
        is_sparse=False,
        coordinates=[1.0, 0, 0.1],
        coordinate_indices=None,
    )
    assert dto.json() == '{"isSparse":false,"coordinates":[1.0,0.0,0.1]}'


def test_json_serialization__vector_sparse():
    dto = VectorDto(
        is_sparse=True,
        coordinates=[1.0, 0.1],
        coordinate_indices=[7, 42],
    )
    assert dto.json() == '{"isSparse":true,"coordinates":[1.0,0.1],"coordinateIndices":[7,42]}'


@pytest.mark.parametrize(
    'dto, expected_json',
    [
        (AttributeDto(key='Str_Key', value=AttributeValueDto(string='Str_Value')),
         '{"key":"Str_Key","value":{"string":"Str_Value"}}'),
        (AttributeDto(key='UuidKey', value=AttributeValueDto(guid=UUID('12345678-1234-1234-1234-123456789abc'))),
         '{"key":"UuidKey","value":{"guid":"12345678-1234-1234-1234-123456789abc"}}'),
        (AttributeDto(key='bool_key', value=AttributeValueDto(bool=True)),
         '{"key":"bool_key","value":{"bool":true}}'),
        (AttributeDto(key='int_key', value=AttributeValueDto(int64=42)),
         '{"key":"int_key","value":{"int64":42}}'),
        (AttributeDto(key='int_key', value=AttributeValueDto(int64=0)),
         '{"key":"int_key","value":{"int64":0}}'),
        (AttributeDto(key='float_key', value=AttributeValueDto(float64=3.1415926)),
         '{"key":"float_key","value":{"float64":3.1415926}}'),
        (AttributeDto(
            key='DateTimeKey',
            value=AttributeValueDto(date_time=datetime(year=2021, month=11, day=23, hour=23, minute=59, second=1))),
         '{"key":"DateTimeKey","value":{"dateTime":"2021-11-23T23:59:01"}}'),
    ]
)
def test_json_serialization__attribute(dto: AttributeDto, expected_json: str):
    assert dto.json() == expected_json


def test_json_serialization__upload_query():
    dto = UploadQueryDto(__root__=[
        InputDataPointDto(
            attributes=[(AttributeDto(key='k', value=AttributeValueDto(bool=False)))],
            vector=None,
            is_deleted=True,
        )
    ])
    assert dto.json() == '[{"attributes":[{"key":"k","value":{"bool":false}}],"isDeleted":true}]'


def test_json_deserialization__error():
    json = '{"errorMessages":["First error message","Second error message"]}'
    expected_dto = ErrorDto(error_messages=['First error message', 'Second error message'])
    assert ErrorDto.parse_raw(json) == expected_dto


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
    expected_dto = SearchResultDto(
        query_vector=VectorDto(is_sparse=False, coordinates=[1.0, 0.0, 0.1]),
        nearest_data_points=[
            FoundDataPointDto(
                vector=VectorDto(is_sparse=False, coordinates=[1.0, 0.0, 0.1]),
                attributes=[AttributeDto(key="Id", value=AttributeValueDto(int64=23))],
                distance=0.0
            ),
            FoundDataPointDto(
                vector=VectorDto(is_sparse=True, coordinates=[-1.0, 0.0, -0.1], coordinate_indices=[7, 0, 42]),
                attributes=[
                    AttributeDto(key="Id", value=AttributeValueDto(int64=-1)),
                    AttributeDto(key="Data", value=AttributeValueDto(string='some payload')),
                ],
                distance=0.2
            ),
        ]
    )
    assert SearchResultDto.parse_raw(json) == expected_dto

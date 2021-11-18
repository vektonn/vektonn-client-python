from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Type
from uuid import UUID

import orjson
from pydantic import BaseModel

from vektonn.utils import camel_case_pydantic_alias_generator, orjson_dumps


class VektonnBaseModel(BaseModel):
    def json(self, **kwargs) -> str:
        return super().json(by_alias=True, exclude_unset=True, exclude_none=True)

    @staticmethod
    def try_parse_json(
        json_string: str,
        result_dto_type: Type[VektonnBaseModel],
    ) -> Optional[VektonnBaseModel]:
        if not json_string:
            return None
        try:
            return result_dto_type.parse_raw(json_string)
        except Exception as err:
            from vektonn.errors import VektonnError
            raise VektonnError(message=f'Failed to parse json: "{json_string}"', inner_exception=err)

    class Config:
        alias_generator = camel_case_pydantic_alias_generator
        allow_population_by_field_name = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ErrorDto(VektonnBaseModel):
    error_messages: List[str]


class VectorDto(VektonnBaseModel):
    is_sparse: bool
    coordinates: List[float]
    coordinate_indices: Optional[List[int]]


class AttributeValueDto(VektonnBaseModel):
    string: Optional[str]
    guid: Optional[UUID]
    bool: Optional[bool]
    int64: Optional[int]
    float64: Optional[float]
    date_time: Optional[datetime]


class AttributeDto(VektonnBaseModel):
    key: str
    value: AttributeValueDto


class SearchQueryDto(VektonnBaseModel):
    split_filter: Optional[List[AttributeDto]]
    query_vectors: List[VectorDto]
    k: int


class FoundDataPointDto(VektonnBaseModel):
    vector: VectorDto
    attributes: List[AttributeDto]
    distance: float


class SearchResultDto(VektonnBaseModel):
    query_vector: VectorDto
    nearest_data_points: List[FoundDataPointDto]


class SearchResultListDto(VektonnBaseModel):
    __root__: List[SearchResultDto]


class InputDataPointDto(VektonnBaseModel):
    attributes: List[AttributeDto]
    vector: Optional[VectorDto]
    is_deleted: bool = False


class UploadQueryDto(VektonnBaseModel):
    __root__: List[InputDataPointDto]

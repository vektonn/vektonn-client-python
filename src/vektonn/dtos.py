from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Type, TypeVar
from uuid import UUID

import orjson
from pydantic import BaseModel

from vektonn.utils import camel_case_pydantic_alias_generator, orjson_dumps

TVektonnModel = TypeVar('TVektonnModel', bound='VektonnBaseModel')


class VektonnBaseModel(BaseModel):
    def json(self, **kwargs) -> str:
        return super().json(by_alias=True, exclude_unset=True, exclude_none=True)

    @staticmethod
    def try_parse_json(
        json_string: str,
        result_dto_type: Type[TVektonnModel],
    ) -> Optional[TVektonnModel]:
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


class ErrorResult(VektonnBaseModel):
    error_messages: List[str]


class Vector(VektonnBaseModel):
    is_sparse: bool
    coordinates: List[float]
    coordinate_indices: Optional[List[int]]


class AttributeValue(VektonnBaseModel):
    string: Optional[str]
    guid: Optional[UUID]
    bool: Optional[bool]
    int64: Optional[int]
    float64: Optional[float]
    date_time: Optional[datetime]


class Attribute(VektonnBaseModel):
    key: str
    value: AttributeValue


class SearchQuery(VektonnBaseModel):
    split_filter: Optional[List[Attribute]]
    query_vectors: List[Vector]
    k: int
    retrieveVectors: bool = True


class FoundDataPoint(VektonnBaseModel):
    vector: Optional[Vector]
    attributes: List[Attribute]
    distance: float


class SearchResult(VektonnBaseModel):
    query_vector: Vector
    nearest_data_points: List[FoundDataPoint]


class SearchResultList(VektonnBaseModel):
    __root__: List[SearchResult]


class InputDataPoint(VektonnBaseModel):
    attributes: List[Attribute]
    vector: Optional[Vector]
    is_deleted: bool = False


class UploadQuery(VektonnBaseModel):
    __root__: List[InputDataPoint]

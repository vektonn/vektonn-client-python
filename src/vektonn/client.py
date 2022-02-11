from typing import Type, Optional, List

import requests
from requests import Response

from vektonn.dtos import (
    TVektonnModel, VektonnBaseModel, ErrorResult,
    SearchQuery, SearchResult, SearchResultList, InputDataPoint, UploadQuery
)
from vektonn.errors import VektonnApiError
from vektonn.service_endpoints import format_search_url, format_upload_url
from vektonn.utils import prepare_request_headers


class Vektonn:
    def __init__(self, base_url: str):
        self._base_url = base_url

    def search(
        self,
        index_name: str,
        index_version: str,
        search_query: SearchQuery,
        request_timeout_seconds: Optional[float] = None,
    ) -> List[SearchResult]:
        url = format_search_url(self._base_url, index_name, index_version)
        search_results = self._post(url, search_query, request_timeout_seconds, result_dto_type=SearchResultList)
        assert search_results is not None
        return search_results.__root__

    def upload(
        self,
        data_source_name: str,
        data_source_version: str,
        input_data_points: List[InputDataPoint],
        request_timeout_seconds: Optional[float] = None,
    ):
        url = format_upload_url(self._base_url, data_source_name, data_source_version)
        query_dto = UploadQuery(__root__=input_data_points)
        self._post(url, query_dto, request_timeout_seconds)

    def _post(
        self,
        url: str,
        query_dto: VektonnBaseModel,
        request_timeout_seconds: Optional[float],
        result_dto_type: Optional[Type[TVektonnModel]] = None,
    ) -> Optional[TVektonnModel]:
        request_content = query_dto.json().encode('utf-8')
        request_headers = prepare_request_headers(request_timeout_seconds)
        response = requests.post(url, headers=request_headers, data=request_content, timeout=request_timeout_seconds)

        if self._is_successful(response):
            if result_dto_type is None:
                return None
            else:
                return VektonnBaseModel.try_parse_json(response.text, result_dto_type)

        raise VektonnApiError(
            status=response.status_code,
            error=VektonnBaseModel.try_parse_json(response.text, result_dto_type=ErrorResult))

    @staticmethod
    def _is_successful(response: Response) -> bool:
        return response.status_code == 200

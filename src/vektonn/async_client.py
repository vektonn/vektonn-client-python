from typing import Type, Optional, List

from aiohttp import ClientResponse, ClientSession

from vektonn.dtos import VektonnBaseModel, ErrorDto, \
    SearchQueryDto, SearchResultDto, SearchResultListDto, InputDataPointDto, UploadQueryDto
from vektonn.errors import VektonnApiError
from vektonn.service_endpoints import format_search_url, format_upload_url


class VektonnAsync:
    _request_headers = {
        'Accept': 'application/json',
        'Content-type': 'application/json',
    }

    def __init__(self, base_url: str):
        self._base_url = base_url

    async def search(
        self,
        index_name: str,
        index_version: str,
        search_query: SearchQueryDto,
    ) -> List[SearchResultDto]:
        url = format_search_url(self._base_url, index_name, index_version)
        search_results = await self._post(url, search_query, result_dto_type=SearchResultListDto)
        return search_results.__root__

    async def upload(
        self,
        data_source_name: str,
        data_source_version: str,
        input_data_points: List[InputDataPointDto],
    ):
        url = format_upload_url(self._base_url, data_source_name, data_source_version)
        query_dto = UploadQueryDto(__root__=input_data_points)
        await self._post(url, query_dto)

    async def _post(
        self,
        url: str,
        query_dto: VektonnBaseModel,
        result_dto_type: Optional[Type[VektonnBaseModel]] = None
    ) -> Optional[VektonnBaseModel]:
        request_content = query_dto.json()
        async with ClientSession() as requests:
            async with requests.post(url, headers=self._request_headers, data=request_content) as response:
                if self._is_successful(response):
                    if result_dto_type is None:
                        return None
                    else:
                        response_text = await response.text()
                        return VektonnBaseModel.try_parse_json(response_text, result_dto_type)

                response_text = await response.text()
                raise VektonnApiError(
                    status=response.status,
                    error=VektonnBaseModel.try_parse_json(response_text, result_dto_type=ErrorDto))

    @staticmethod
    def _is_successful(response: ClientResponse) -> bool:
        return response.status == 200

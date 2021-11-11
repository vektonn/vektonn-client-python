from typing import Type, Optional, List

from aiohttp import ClientResponse, ClientSession

from vektonn.dtos import VektonnBaseModel, ErrorDto, \
    SearchQueryDto, SearchResultDto, SearchResultListDto, InputDataPointDto, UploadQueryDto
from vektonn.errors import VektonnApiError
from vektonn.service_endpoints import format_search_url, format_upload_url
from vektonn.utils import assert_is_instance


class VektonnAsync:
    _base_url: str
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
        return assert_is_instance(search_results, SearchResultListDto).__root__

    async def upload(
        self,
        data_source_name: str,
        data_source_version: str,
        input_data_points: List[InputDataPointDto],
    ):
        url = format_upload_url(self._base_url, data_source_name, data_source_version)
        query_dto = UploadQueryDto(__root__=input_data_points)
        await self._post(url, query_dto, result_dto_type=None)

    async def _post(
        self,
        url: str,
        query_dto: VektonnBaseModel,
        result_dto_type: Optional[Type[VektonnBaseModel]]
    ) -> Optional[VektonnBaseModel]:
        request_content = query_dto.json()
        async with ClientSession() as requests:
            async with requests.post(url, headers=self._request_headers, data=request_content) as response:
                if self._is_successful(response):
                    if result_dto_type is None:
                        return None
                    else:
                        response_text = await response.text()
                        return result_dto_type.parse_raw(response_text)

                raise VektonnApiError(
                    status=response.status,
                    error=ErrorDto.parse_raw(await response.text()))

    @staticmethod
    def _is_successful(response: ClientResponse) -> bool:
        return response.status == 200

import pytest

from tests import zero_vector, index_name, index_version, data_source_name, data_source_version, is_vektonn_running
from vektonn import VektonnAsync, VektonnApiError
from vektonn.dtos import SearchQueryDto, SearchResultDto, InputDataPointDto, AttributeDto, AttributeValueDto, ErrorDto

pytestmark = pytest.mark.skipif(is_vektonn_running is not True, reason="Integration tests require Vektonn running")


async def test_search__success(vektonn_client_async: VektonnAsync):
    search_query = SearchQueryDto(k=1, query_vectors=[zero_vector])
    search_results = await vektonn_client_async.search(index_name, index_version, search_query)
    assert search_results[0] == SearchResultDto(
        query_vector=search_query.query_vectors[0],
        nearest_data_points=[],
    )


async def test_search__index_does_not_exist(vektonn_client_async: VektonnAsync):
    non_existing_index_name = 'Non-existing.Index'
    search_query = SearchQueryDto(k=1, query_vectors=[zero_vector])
    with pytest.raises(VektonnApiError) as error_info:
        await vektonn_client_async.search(non_existing_index_name, index_version, search_query)
    assert error_info.value.status == 404
    assert isinstance(error_info.value.error, ErrorDto)
    assert error_info.value.error.error_messages == [
        f'Index IndexId {{ Name = {non_existing_index_name}, Version = {index_version} }} does not exist'
    ]


async def test_search__bad_request(vektonn_client_async: VektonnAsync):
    search_query = SearchQueryDto(k=-1, query_vectors=[])
    with pytest.raises(VektonnApiError) as error_info:
        await vektonn_client_async.search(index_name, index_version, search_query)
    assert error_info.value.status == 400
    assert isinstance(error_info.value.error, ErrorDto)
    assert error_info.value.error.error_messages == [
        'K must be positive',
        'At least one query vector is required',
    ]


async def test_upload__success(vektonn_client_async: VektonnAsync):
    input_data_points = [
        InputDataPointDto(
            attributes=[
                AttributeDto(key='Id', value=AttributeValueDto(int64=42)),
                AttributeDto(key='SplitId', value=AttributeValueDto(bool=True)),
                AttributeDto(key='Payload', value=AttributeValueDto(string='la-la-la and some unicode chars Ὀδύσσεια 曳航')),
            ],
            is_deleted=True,
        )
    ]
    await vektonn_client_async.upload(data_source_name, data_source_version, input_data_points)


async def test_upload__data_source_does_not_exist(vektonn_client_async: VektonnAsync):
    non_existing_data_source_name = 'Non-existing.Source'
    input_data_points = [
        InputDataPointDto(
            attributes=[AttributeDto(key='Id', value=AttributeValueDto(int64=42))],
            is_deleted=True,
        )
    ]
    with pytest.raises(VektonnApiError) as error_info:
        await vektonn_client_async.upload(non_existing_data_source_name, data_source_version, input_data_points)
    assert error_info.value.status == 404
    assert isinstance(error_info.value.error, ErrorDto)
    assert error_info.value.error.error_messages == [
        f'Data source DataSourceId {{ Name = {non_existing_data_source_name}, Version = {data_source_version} }} does not exist'
    ]


async def test_upload__bad_request(vektonn_client_async: VektonnAsync):
    input_data_points = [
        InputDataPointDto(
            attributes=[
                AttributeDto(key='Id', value=AttributeValueDto(int64=42)),
                AttributeDto(key='SplitId', value=AttributeValueDto(bool=True)),
                AttributeDto(key='Payload', value=AttributeValueDto(string='la-la-la')),
            ],
            is_deleted=False,
        )
    ]
    with pytest.raises(VektonnApiError) as error_info:
        await vektonn_client_async.upload(data_source_name, data_source_version, input_data_points)
    assert error_info.value.status == 400
    assert isinstance(error_info.value.error, ErrorDto)
    assert error_info.value.error.error_messages == ['IsDeleted is inconsistent with Vector']

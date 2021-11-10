import pytest

from vektonn import Vektonn, VektonnApiError
from vektonn.dtos import SearchQueryDto, VectorDto, SearchResultDto, InputDataPointDto, AttributeDto, AttributeValueDto

data_source_name = 'Samples.DenseVectors'
data_source_version = '0.1'
index_name = 'Samples.DenseVectors'
index_version = '0.1'
zero_vector = VectorDto(is_sparse=False, coordinates=[0.0, 0.0])


def test_search__success(vektonn_client: Vektonn):
    search_query = SearchQueryDto(k=1, query_vectors=[zero_vector])
    search_results = vektonn_client.search(index_name, index_version, search_query)
    assert search_results[0] == SearchResultDto(
        query_vector=search_query.query_vectors[0],
        nearest_data_points=[],
    )


def test_search__index_does_not_exist(vektonn_client: Vektonn):
    non_existing_index_name = 'Non-existing.Index'
    search_query = SearchQueryDto(k=1, query_vectors=[zero_vector])
    with pytest.raises(VektonnApiError) as error_info:
        vektonn_client.search(non_existing_index_name, index_version, search_query)
    assert error_info.value.status == 404
    assert error_info.value.error.error_messages == [
        f'Index IndexId {{ Name = {non_existing_index_name}, Version = {index_version} }} does not exist'
    ]


def test_search__bad_request(vektonn_client: Vektonn):
    search_query = SearchQueryDto(k=-1, query_vectors=[])
    with pytest.raises(VektonnApiError) as error_info:
        vektonn_client.search(index_name, index_version, search_query)
    assert error_info.value.status == 400
    assert error_info.value.error.error_messages == [
        'K must be positive',
        'At least one query vector is required',
    ]


def test_upload__success(vektonn_client: Vektonn):
    input_data_points = [
        InputDataPointDto(
            attributes=[
                AttributeDto(key='Id', value=AttributeValueDto(int64=42)),
                AttributeDto(key='SplitId', value=AttributeValueDto(bool=True)),
                AttributeDto(key='Payload', value=AttributeValueDto(string='la-la-la')),
            ],
            is_deleted=True,
        )
    ]
    vektonn_client.upload(data_source_name, data_source_version, input_data_points)


def test_upload__data_source_does_not_exist(vektonn_client: Vektonn):
    non_existing_data_source_name = 'Non-existing.Source'
    input_data_points = [
        InputDataPointDto(
            attributes=[AttributeDto(key='Id', value=AttributeValueDto(int64=42))],
            is_deleted=True,
        )
    ]
    with pytest.raises(VektonnApiError) as error_info:
        vektonn_client.upload(non_existing_data_source_name, data_source_version, input_data_points)
    assert error_info.value.status == 404
    assert error_info.value.error.error_messages == [
        f'Data source DataSourceId {{ Name = {non_existing_data_source_name}, Version = {data_source_version} }} does not exist'
    ]


def test_upload__bad_request(vektonn_client: Vektonn):
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
        vektonn_client.upload(data_source_name, data_source_version, input_data_points)
    assert error_info.value.status == 400
    assert error_info.value.error.error_messages == ['IsDeleted is inconsistent with Vector']

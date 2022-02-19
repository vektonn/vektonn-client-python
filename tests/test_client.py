from time import sleep

import pytest

from tests import (
    is_vektonn_running, index_name, index_version, data_source_name, data_source_version, zero_vector,
    dense_vector, input_data_point, found_data_point
)
from vektonn import Vektonn, VektonnApiError
from vektonn.dtos import (
    Attribute, AttributeValue, SearchQuery, SearchResult, InputDataPoint, ErrorResult
)

pytestmark = pytest.mark.skipif(is_vektonn_running is not True, reason="Integration tests require Vektonn running")


def test_search__success(vektonn_client: Vektonn):
    input_data_points = [
        input_data_point(vector=[0.0, 1.0], dp_id=1, payload='first data point'),
        input_data_point(vector=[1.0, 0.0], dp_id=2, payload='second data point'),
        input_data_point(vector=[-0.5, 0.0], dp_id=3, payload='third data point'),
    ]
    vektonn_client.upload(data_source_name, data_source_version, input_data_points)
    sleep(1)  # wait for Vektonn data indexing

    search_query = SearchQuery(k=2, query_vectors=[dense_vector([0.0, 2.0])], retrieveVectors=True)
    expected_nearest_data_points = [
        found_data_point(distance=1.0, vector=[0.0, 1.0], dp_id=1, payload='first data point'),
        found_data_point(distance=4.25, vector=[-0.5, 0.0], dp_id=3, payload='third data point'),
    ]

    search_results = vektonn_client.search(index_name, index_version, search_query, request_timeout_seconds=1)
    assert search_results[0] == SearchResult(
        query_vector=search_query.query_vectors[0],
        nearest_data_points=expected_nearest_data_points,
    )

    search_query.retrieveVectors = False
    for i, nearest_data_point in enumerate(expected_nearest_data_points):
        expected_nearest_data_points[i].vector = None

    search_results = vektonn_client.search(index_name, index_version, search_query, request_timeout_seconds=1)
    assert search_results[0] == SearchResult(
        query_vector=search_query.query_vectors[0],
        nearest_data_points=expected_nearest_data_points)

    for i, idp in enumerate(input_data_points):
        input_data_points[i].vector = None
        input_data_points[i].is_deleted = True
    vektonn_client.upload(data_source_name, data_source_version, input_data_points)
    sleep(1)  # wait for Vektonn data indexing


def test_search__success_empty_index(vektonn_client: Vektonn):
    search_query = SearchQuery(k=1, query_vectors=[zero_vector])
    search_results = vektonn_client.search(index_name, index_version, search_query, request_timeout_seconds=1)
    assert search_results[0] == SearchResult(
        query_vector=search_query.query_vectors[0],
        nearest_data_points=[],
    )


def test_search__index_does_not_exist(vektonn_client: Vektonn):
    non_existing_index_name = 'Non-existing.Index'
    search_query = SearchQuery(k=1, query_vectors=[zero_vector])
    with pytest.raises(VektonnApiError) as error_info:
        vektonn_client.search(non_existing_index_name, index_version, search_query)
    assert error_info.value.status == 404
    assert isinstance(error_info.value.error, ErrorResult)
    assert error_info.value.error.error_messages == [
        f'Index IndexId {{ Name = {non_existing_index_name}, Version = {index_version} }} does not exist'
    ]


def test_search__bad_request(vektonn_client: Vektonn):
    search_query = SearchQuery(k=-1, query_vectors=[])
    with pytest.raises(VektonnApiError) as error_info:
        vektonn_client.search(index_name, index_version, search_query)
    assert error_info.value.status == 400
    assert isinstance(error_info.value.error, ErrorResult)
    assert error_info.value.error.error_messages == [
        'K must be positive',
        'At least one query vector is required',
    ]


def test_upload__success(vektonn_client: Vektonn):
    input_data_points = [
        InputDataPoint(
            attributes=[
                Attribute(key='id', value=AttributeValue(int64=42)),
                Attribute(key='payload', value=AttributeValue(string='la-la-la and some unicode chars Ὀδύσσεια 曳航')),
            ],
            is_deleted=True,
        )
    ]
    vektonn_client.upload(data_source_name, data_source_version, input_data_points)


def test_upload__data_source_does_not_exist(vektonn_client: Vektonn):
    non_existing_data_source_name = 'Non-existing.Source'
    input_data_points = [
        InputDataPoint(
            attributes=[Attribute(key='id', value=AttributeValue(int64=42))],
            is_deleted=True,
        )
    ]
    with pytest.raises(VektonnApiError) as error_info:
        vektonn_client.upload(non_existing_data_source_name, data_source_version, input_data_points)
    assert error_info.value.status == 404
    assert isinstance(error_info.value.error, ErrorResult)
    assert error_info.value.error.error_messages == [
        f'Data source DataSourceId {{ Name = {non_existing_data_source_name}, Version = {data_source_version} }} does not exist'
    ]


def test_upload__bad_request(vektonn_client: Vektonn):
    input_data_points = [
        InputDataPoint(
            attributes=[
                Attribute(key='id', value=AttributeValue(int64=42)),
                Attribute(key='payload', value=AttributeValue(string='la-la-la')),
            ],
            is_deleted=False,
        )
    ]
    with pytest.raises(VektonnApiError) as error_info:
        vektonn_client.upload(data_source_name, data_source_version, input_data_points)
    assert error_info.value.status == 400
    assert isinstance(error_info.value.error, ErrorResult)
    assert error_info.value.error.error_messages == ['IsDeleted is inconsistent with Vector']

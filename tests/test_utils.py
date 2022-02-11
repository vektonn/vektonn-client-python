import pytest

from vektonn.utils import camel_case_pydantic_alias_generator, prepare_request_headers


@pytest.mark.parametrize(
    'input_string, expected_output',
    [
        ('snake_case', 'snakeCase'),
        ('alreadyCamelCase', 'alreadyCamelCase'),
        ('PascalCase', 'PascalCase'),
        ('__root__', '__root__'),
    ]
)
def test_camel_case_pydantic_alias_generator(input_string: str, expected_output: str):
    assert camel_case_pydantic_alias_generator(input_string) == expected_output


def test_prepare_request_headers():
    assert prepare_request_headers(request_timeout_seconds=10) == {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
        'Request-Timeout': '10.000',
    }
    assert prepare_request_headers() == {
        'Accept': 'application/json',
        'Content-Type': 'application/json; charset=utf-8',
    }
    assert prepare_request_headers(request_timeout_seconds=1.001)['Request-Timeout'] == '1.001'
    assert prepare_request_headers(request_timeout_seconds=1.0001)['Request-Timeout'] == '1.000'
    assert prepare_request_headers(request_timeout_seconds=3.1415)['Request-Timeout'] == '3.142'

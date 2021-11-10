import pytest

from vektonn.utils import camel_case_pydantic_alias_generator


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

from typing import Type, TypeVar, Any

import orjson


def camel_case_pydantic_alias_generator(string: str) -> str:
    if string.startswith('__'):  # handle e.g. __root__ pydantic field
        return string
    string_split = string.split('_')
    return string_split[0] + ''.join(word.capitalize() for word in string_split[1:])


def orjson_dumps(obj: Any, *, default) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(obj, default=default).decode()


TClass = TypeVar('TClass')


def assert_is_instance(obj: object, cls: Type[TClass]) -> TClass:
    if not isinstance(obj, cls):
        raise TypeError(f'obj is not an instance of cls: obj={obj} cls={cls}')
    return obj
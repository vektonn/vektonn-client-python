from typing import Any, Optional

import orjson

_request_headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=utf-8',
}


def prepare_request_headers(request_timeout_seconds: Optional[float] = None):
    if request_timeout_seconds is None:
        return _request_headers
    else:
        return {**_request_headers, 'Request-Timeout': f'{request_timeout_seconds:.3f}'}


def camel_case_pydantic_alias_generator(string: str) -> str:
    if string.startswith('__'):  # handle e.g. __root__ pydantic field
        return string
    string_split = string.split('_')
    return string_split[0] + ''.join(word.capitalize() for word in string_split[1:])


def orjson_dumps(obj: Any, *, default) -> str:
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(obj, default=default).decode()

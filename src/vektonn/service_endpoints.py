def format_search_url(base_url: str, index_name: str, index_version: str) -> str:
    return f'{base_url.rstrip("/")}/api/v1/search/{index_name}/{index_version}'


def format_upload_url(base_url: str, data_source_name: str, data_source_version: str) -> str:
    return f'{base_url.rstrip("/")}/api/v1/upload/{data_source_name}/{data_source_version}'

import pytest

from tests import vektonn_local_base_url
from vektonn import Vektonn, VektonnAsync

pytest_plugins = "aiohttp.pytest_plugin"


@pytest.fixture(scope="session")
def vektonn_client() -> Vektonn:
    return Vektonn(vektonn_local_base_url)


@pytest.fixture(scope="session")
def vektonn_client_async() -> VektonnAsync:
    return VektonnAsync(vektonn_local_base_url)

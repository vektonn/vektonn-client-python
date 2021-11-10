import pytest

from vektonn import Vektonn

vektonn_local_base_url = 'http://localhost:8081'


@pytest.fixture(scope="session")
def vektonn_client() -> Vektonn:
    return Vektonn(vektonn_local_base_url)

# Python client for Vektonn

[![CI](https://github.com/vektonn/vektonn-client-python/actions/workflows/ci.yml/badge.svg)](https://github.com/vektonn/vektonn-client-python/actions/workflows/ci.yml)
[![version](https://img.shields.io/pypi/v/vektonn.svg?color=blue)](https://pypi.org/project/vektonn/)
[![Supported Python Versions](https://img.shields.io/pypi/pyversions/vektonn?logo=python&logoColor=blue)](https://pypi.org/project/vektonn/)
[![license](https://img.shields.io/hexpm/l/plug.svg?color=green)](https://github.com/vektonn/vektonn-client-python/blob/master/LICENSE)

**Vektonn** is a high-performance battle-tested [kNN vector search](https://en.wikipedia.org/wiki/Nearest_neighbor_search#k-nearest_neighbors) engine for your data science applications.
It helps you manage vectors' lifecycle and radically reduces time to market.

See [documentation](https://vektonn.github.io/vektonn/) for more info.

## Installation

Install the latest version:
```shell
$ pip install vektonn
```

Install specific version:
```shell
$ pip install vektonn==1.2.3
```

Upgrade to the latest version:
```shell
$ pip install --upgrade vektonn
```

## Usage

Having Vektonn running on `localhost:8081` and configured for [QuickStart](https://github.com/vektonn/vektonn-examples/tree/master/quick-start) examples one can access it with synchronous Python client:

```python
from vektonn import Vektonn

vektonn_client = Vektonn('http://localhost:8081')
```

or asynchronous one:

```python
from vektonn import VektonnAsync

vektonn_client_async = VektonnAsync('http://localhost:8081')
```

To upload data to Vektonn use `upload()` method:

```python
from vektonn.dtos import Attribute, AttributeValue, InputDataPoint, Vector

vektonn_client.upload(
    data_source_name='QuickStart.Source',
    data_source_version='1.0',
    input_data_points=[
        InputDataPoint(
            attributes=[
                Attribute(key='id', value=AttributeValue(int64=1)),
                Attribute(key='payload', value=AttributeValue(string='sample data point')),
            ],
            vector=Vector(is_sparse=False, coordinates=[3.14, 2.71]))
    ])
```

To query Vektonn for `k` nearest data points to the given `query_vector` use `search()` method:

```python
from vektonn.dtos import Vector, SearchQuery

k = 10
query_vector = Vector(is_sparse=False, coordinates=[1.2, 3.4])

search_results = vektonn_client.search(
    index_name='QuickStart.Index',
    index_version='1.0',
    search_query=SearchQuery(k=k, query_vectors=[query_vector]))

print(f'For query vector {query_vector.coordinates} {k} nearest data points are:')
for fdp in search_results[0].nearest_data_points:
    attrs = {x.key: x.value for x in fdp.attributes}
    distance, vector, dp_id, payload = fdp.distance, fdp.vector, attrs['id'].int64, attrs['payload'].string
    print(f' - "{payload}" with id = {dp_id}, vector = {vector.coordinates}, distance = {distance}')
```

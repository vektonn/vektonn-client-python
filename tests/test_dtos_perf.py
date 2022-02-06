import cProfile
import sys

import numpy as np
import pytest

from vektonn.dtos import (
    Attribute, AttributeValue, Vector, InputDataPoint
)


def test_fast_construct():
    vector = np.random.rand(5)
    p1 = to_idp(42, vector)
    p2 = to_idp_fast(42, vector)
    assert p1 == p2
    assert p1.json() == p2.json()


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python 3.8 or higher")
def test_perf_construct():
    vectors = np.random.rand(1183514 // 10, 100)
    with cProfile.Profile() as pr:
        construct(vectors)
    pr.print_stats(sort='time')


@pytest.mark.skipif(sys.version_info < (3, 8), reason="requires python 3.8 or higher")
def test_perf_serialize():
    vectors = np.random.rand(1183514 // 10, 100)
    with cProfile.Profile() as pr:
        input_data_points = construct(vectors)
        serialize(input_data_points)
    pr.print_stats(sort='time')


def serialize(input_data_points):
    for idp in input_data_points:
        idp.json()


def construct(vectors: np.ndarray):
    input_data_points = []
    for ind, vector in enumerate(vectors):
        input_data_points.append(to_idp_fast(ind, vector))
    return input_data_points


def to_idp(ind, vector):
    return InputDataPoint(
        attributes=[Attribute(key='id', value=AttributeValue(int64=ind))],
        vector=Vector(is_sparse=False, coordinates=vector.tolist()))


def to_idp_fast(ind, vector):
    return InputDataPoint.construct(
        attributes=[Attribute.construct(key='id', value=AttributeValue.construct(int64=ind))],
        vector=Vector.construct(is_sparse=False, coordinates=vector.tolist()))

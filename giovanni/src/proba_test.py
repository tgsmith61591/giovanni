# -*- coding: utf-8 -*-

import numpy as np

from giovanni.src import proba

from unittest import mock
from numpy.testing import assert_almost_equal
import pytest

base_rate = 1 / 8192.


@pytest.mark.parametrize(
    'rate,n_tries,swarm_size,expected', [

        pytest.param(base_rate, 0, 1, 0),
        pytest.param(base_rate, 1, 1, base_rate),
        pytest.param(base_rate, 1, 3, 0.0003662),  # gen IV starter
        pytest.param(base_rate, 1, (1, 3), (base_rate, 0.0003662)),

    ]
)
def test_compute_sr_proba(rate, n_tries, swarm_size, expected):
    actual = proba.compute_sr_proba(rate, n_tries, swarm_size)
    assert_almost_equal(expected, actual)


def test_compute_sr_proba_error():
    with pytest.raises(ValueError):
        proba.compute_sr_proba(base_rate, 1, 0)


class MockRandomState:
    v = None
    
    def __init__(self, *_):
        pass

    def rand(self, *_):
        return self.v


def test_sim_batch_first():
    rate = 1. / 8192.
    swarm_size = 1
    batch_size = 10000

    with mock.patch("numpy.random.RandomState", MockRandomState) as mrs:
        mrs.v = 1e-12 * np.ones((batch_size, swarm_size))
        actual_encounter = proba.simulate_sr_for_encounter(
            rate, swarm_size, batch_size,
        )

    assert 1 == actual_encounter


def test_sim_batch_last():
    rate = 1. / 8192.
    swarm_size = 1
    batch_size = 10000

    with mock.patch("numpy.random.RandomState", MockRandomState) as mrs:
        mrs.v = np.ones((batch_size, swarm_size))
        mrs.v[-1, 0] = 1e-12

        actual_encounter = proba.simulate_sr_for_encounter(
            rate, swarm_size, batch_size,
        )

    assert batch_size == actual_encounter

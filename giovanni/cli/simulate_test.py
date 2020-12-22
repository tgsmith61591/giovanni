# -*- coding: utf-8 -*-

import numpy as np
from unittest import mock
from giovanni.cli import simulate


class MockRandomState:
    v = None

    def rand(self, *_):
        return self.v


def test_sim_batch_first():
    rate = 1. / 8192.
    swarm_size = 1
    batch_size = 10000

    with mock.patch("numpy.random.RandomState", MockRandomState) as mrs:
        mrs.v = 1e-12 * np.ones((batch_size, swarm_size))
        actual_encounter = simulate._simulation(rate, swarm_size, batch_size)

    assert 1 == actual_encounter


def test_sim_batch_last():
    rate = 1. / 8192.
    swarm_size = 1
    batch_size = 10000

    with mock.patch("numpy.random.RandomState", MockRandomState) as mrs:
        mrs.v = np.ones((batch_size, swarm_size))
        mrs.v[-1, 0] = 1e-12

        actual_encounter = simulate._simulation(rate, swarm_size, batch_size)

    assert batch_size == actual_encounter

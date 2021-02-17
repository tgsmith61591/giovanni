# -*- coding: utf-8 -*-

import numpy as np

__all__ = [
    'compute_sr_proba',
]


def compute_sr_proba(rate, n_tries, swarm_size=1):
    """Compute the probability of a shiny after `n_tries`

    Parameters
    ----------
    rate : float
        The base shiny encounter rate. This is determined by the generation,
        hunting method, and whether you have a charm equipped.

    n_tries : int
        The number of SRs performed up to this point.

    swarm_size : int, optional (default=1)
        The size of the swarm, for generations where there is a swarm. For
        Gen IV, this could also be 3 for the starters, where any/all could be
        shiny. If populated, the probability returned is the probability that
        ANY of the 'mons in the swarm is shiny.
    """
    # If computing for a range of swarm sizes
    if isinstance(swarm_size, (tuple, list)):
        return tuple(compute_sr_proba(rate, n_tries, sz) for sz in swarm_size)

    if swarm_size < 1:
        raise ValueError("swarm_size must be a positive integer")

    p_no_encounter_single = (1. - rate) ** swarm_size
    p_no_encouter = p_no_encounter_single ** n_tries
    return 1 - p_no_encouter


def simulate_sr_for_encounter(rate, swarm_size=1, batch_size=10000, seed=None):
    """Simulate the number of SRs required for a shiny encounter

    To be used when performing random monte-carlo simulation. Finds the number
    of encounters required for a single shiny encounter.

    Parameters
    ----------
    rate : float
        The base shiny encounter rate. This is determined by the generation,
        hunting method, and whether you have a charm equipped.

    swarm_size : int, optional (default=1)
        The size of the swarm, for generations where there is a swarm. For
        Gen IV, this could also be 3 for the starters, where any/all could be
        shiny. If populated, the probability returned is the probability that
        ANY of the 'mons in the swarm is shiny.

    batch_size : int, optional (default=10000)
        The size of mini-batches to simulate over. Will continue to generate
        batches until a shiny is encountered.

    seed : int or None, optional (default=None)
        The seed for the random state.

    Examples
    --------
    >>> from giovanni.src import proba
    >>> proba.simulate_sr_for_encounter(1/8192., 3, seed=42)  # gen IV starter
    968
    """
    arange = np.arange(batch_size)
    rs = np.random.RandomState(seed)

    # TODO: cython would be cool to speed this up
    def _sim_batch(n):
        """
        Generate a batch of random numbers. It is faster to compute
        randoms in a batch than it is one by one. Once this random generator
        is exhausted, generate a new one.
        """
        batch = rs.rand(n, swarm_size)
        mask = np.any(batch < rate, axis=1)

        if not mask.any():
            return None

        # Get the first scenario it finds
        return arange[mask][0]

    i = 1
    while True:
        which_idx = _sim_batch(batch_size)

        if which_idx is None:
            i += batch_size
        else:
            i += which_idx
            return i

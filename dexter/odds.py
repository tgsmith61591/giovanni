# -*- coding: utf-8 -*-

"""
Get odds for the generations

TODO: Wishlist
  . Support roman numerals for generations
  . Masuda method
  . Radar rates
"""

__all__ = [
    'get_base_odds',
]

_base_rates = {
    1: 0.,
    2: 1. / 8192.,
    3: 1. / 8192.,
    4: 1. / 8192.,
    5: 1. / 8192.,
    6: 1. / 4096.,
    7: 1. / 4096.,
}

_charm_multiplier = {
    1: 1.,
    2: 1.,
    3: 1.,
    4: 1.,

    # not present in 1-4
    5: 2.,
    6: 2.,
    7: 2.,
}



def get_base_odds(gen, charm):
    """Get the shiny odds for a generation

    Parameters
    ----------
    gen : int
        The generation/version being played. There are different odds for each.

    charm : bool
        Whether the shiny charm is equipped

    Returns
    -------
    odds : float
        The probability that any SR will result in a shiny appearing.
    """
    if gen not in _base_rates:
        raise ValueError(f"Unknown generation: {gen}")

    multiplier = 1.
    if charm:
        multiplier = _charm_multiplier[gen]

    return _base_rates[gen] * multiplier

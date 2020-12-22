# -*- coding: utf-8 -*-

"""
Main module and argparser for the `simulate` command

    $ dexter simulate <options>
"""

import numpy as np
import pandas as pd

import textwrap
import tqdm

from dexter.cli import common
from dexter import odds
from dexter import utils


def configure_subparser(subparsers):
    """Create the parser for the `simulate` commands"""
    description = textwrap.dedent("""
    Simulates the number of soft resets needed to encounter a shiny, producing
    a plot and statistics.
    """)

    example = textwrap.dedent("""
    Examples:

        $ dexter simulate --gen 4 -n 100
    """)

    p = subparsers.add_parser(
        "simulate",
        description=description,
        help=description,
        epilog=example,
    )

    _, optional_args = common.get_argument_groups(p, "simulate")
    optional_args.add_argument(
        "-n", "--num",
        dest="num",
        type=int,
        help="The number of simulations to perform. If not provided, will "
             "default to 1000",
    )

    p.set_defaults(
        num=1000,
    )


def do_call(args):
    """Call the `simulate` CLI entrypoint"""
    level = common.get_logging_level(args, "INFO")
    logger = utils.get_logger(__name__, level=level)

    gen = common.parse_generation(args)

    num_sim = args.num
    swarm_size = args.swarm_size
    charm = args.charm

    if num_sim < 1:
        raise ValueError("--num must be a positive integer")

    logger.debug(f"Num simulations: {num_sim}")
    logger.debug(f"Swarm size: {swarm_size}")
    logger.debug(f"Shiny charm: {charm}")

    base_rate = odds.get_base_odds(gen, charm)
    logger.debug(f"Generation: {gen} (base rate={base_rate:.6f})")

    simulations = []
    for _ in tqdm.tqdm(range(num_sim), desc="simulation"):
        simulations.append(_simulation(base_rate, swarm_size))

    simulations = np.asarray(simulations)
    name = f"Required encounters (gen={gen}, " \
           f"num_trials={num_sim}, " \
           f"swarm_size={swarm_size})"

    table = pd.Series({
        "Average": np.round(np.average(simulations), 3),
        "Std Dev": np.round(np.std(simulations), 3),
        "Max": np.max(simulations),
        "Min": np.min(simulations),
    }, name=name)

    logger.info(
        f"Montecarlo simulation results --\n{table}"
    )

    return 0


def _simulation(rate, swarm_size, batch_size=10000):
    """Calculate the number of SRs required for a single simulation"""
    arange = np.arange(batch_size)
    rs = np.random.RandomState()

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

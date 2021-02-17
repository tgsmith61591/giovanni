# -*- coding: utf-8 -*-

"""
Main module and argparser for the `simulate` command

    $ giovanni simulate <options>
"""

import numpy as np
import pandas as pd

import textwrap
import tqdm

from giovanni.cli import common
from giovanni import base
from giovanni.src import proba as proba_lib
from giovanni import utils


def configure_subparser(subparsers):
    """Create the parser for the `simulate` commands"""
    description = textwrap.dedent("""
    Simulates the number of soft resets needed to encounter a shiny, producing
    a plot and statistics.
    """)

    example = textwrap.dedent("""
    Examples:

        $ giovanni simulate --gen 4 -n 100
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

    base_rate = base.get_base_odds(gen, charm)
    logger.debug(f"Generation: {gen} (base rate={base_rate:.6f})")

    simulations = []
    for _ in tqdm.tqdm(range(num_sim), desc="simulation"):
        simulations.append(
            # TODO: seeds?
            proba_lib.simulate_sr_for_encounter(base_rate, swarm_size),
        )

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

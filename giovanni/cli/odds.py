# -*- coding: utf-8 -*-

"""
Main module and argparser for the probability/odds commands

    $ giovanni odds <options>
"""

import textwrap

from giovanni.cli import common
from giovanni import odds
from giovanni import utils


def configure_subparser(subparsers):
    """Create the parser for the `odds` commands"""
    description = textwrap.dedent("""
    Calculate the odds of having encountered a shiny after a given number of
    soft-resets.
    """)

    example = textwrap.dedent("""
    Examples:

        $ giovanni odds --gen 4 --soft_resets 100
    """)

    p = subparsers.add_parser(
        "odds",
        description=description,
        help=description,
        epilog=example,
    )

    _, optional_args = common.get_argument_groups(p, "odds")
    optional_args.add_argument(
        "-r", "--soft_resets",
        dest="soft_resets",
        type=int,
        help="The number of soft resets to use in the odds calculation. If "
             "not provided, will default to 1",
    )

    p.set_defaults(
        soft_resets=1,
    )


def do_call(args):
    """Call the `odds` CLI entrypoint"""
    level = common.get_logging_level(args, "INFO")
    logger = utils.get_logger(__name__, level=level)

    gen = common.parse_generation(args)

    num_sr = args.soft_resets
    swarm_size = args.swarm_size
    charm = args.charm

    logger.debug(f"Num soft resets: {num_sr}")
    logger.debug(f"Swarm size: {swarm_size}")
    logger.debug(f"Shiny charm: {charm}")

    base_rate = odds.get_base_odds(gen, charm)
    logger.debug(f"Generation: {gen} (base rate={base_rate:.6f})")

    proba = 100 * _get_proba(
        base_rate, num_sr, swarm_size=swarm_size,
    )

    logger.info(
        f"Odds of shiny encounter after {num_sr:,} soft "
        f"reset{'s' if num_sr > 1 else ''}: {proba:.3f}%"
    )

    return 0


def _get_proba(rate, n_tries, swarm_size):
    """Compute the probability"""
    p_no_encounter_single = (1. - rate) ** swarm_size
    p_no_encouter = p_no_encounter_single ** n_tries
    return 1 - p_no_encouter

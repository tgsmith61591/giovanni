# -*- coding: utf-8 -*-

"""
Simulate shiny encounter rates

giovanni provides the following commands:

    Information
    ===========

    help      : display a list of available giovanni commands and their help
                information

    Simulations
    ===========

    simulate  : simulates a sequence of soft-resets for a given generation,
                producing a distribution of number of required resets


    Probability
    ===========

    odds      : calculate the probability of encountering a shiny by a given
                SR count

Additional help for each command can be accessed by using:

    giovanni <command> -h
"""

import sys

from giovanni.cli import odds, simulate, parsers, common
from giovanni import utils


def main():
    """Run the module"""
    p = parsers.generate_parser()
    args = p.parse_args()

    # Use debug mode if verbose is set
    level = common.get_logging_level(args, "INFO")
    logger = utils.get_logger(__name__, level=level)

    mod_name = args.cmd
    logger.debug(f"Calling giovanni.cli.{mod_name}.do_call")

    # Determine which command was run, delegate to its submodule
    if mod_name == "odds":
        exit_code = odds.do_call(args)
    elif mod_name == "simulate":
        exit_code = simulate.do_call(args)
    else:
        raise RuntimeError(
            f"Internal error, unknown command: {mod_name}. Please report this "
            f"as an issue to the developers!"
        )

    sys.exit(exit_code)

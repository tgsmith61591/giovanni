# -*- coding: utf-8 -*-

"""Constants used by parsers/subparsers alike"""

_VERBOSE = """Be verbose in how odds/simulations are calculated."""
_GEN = """The generation game to simulate"""


def get_argument_groups(p, cmd):
    """Get the common required and optional arguments groups"""
    required_args = p.add_argument_group(f"{cmd} required")
    required_args.add_argument(
        "-g", "--gen",
        dest="gen",
        type=int,  # TODO: if roman in future, change to str
        help="The generation",
    )

    optional_args = p.add_argument_group(f"{cmd} optional")
    optional_args.add_argument(
        "--verbose",
        action="store_true",
        help=_VERBOSE,
    )

    optional_args.add_argument(
        "-s", "--swarm_size",
        dest="swarm_size",
        type=int,
        help="The size of the pokemon swarm, or candidate 'mons. For instance,"
             "if the swarm size is 5, will compute the likelihood or number "
             "of required resets until AT LEAST ONE of the swarm is shiny. If "
             "not provided, will default to 1",
    )

    optional_args.add_argument(
        "--charm",
        action="store_true",
        help="Whether the shiny charm is equipped. This is only applicable in "
             "gen 5+",
    )

    p.set_defaults(
        swarm_size=1,
        charm=False,
        verbose=False,
    )

    return required_args, optional_args


def get_logging_level(args, default="INFO"):
    """Get the logging level from the CLI args"""
    verbose = args.verbose
    if verbose:
        return "DEBUG"
    return default


def parse_generation(args):
    """Parse the `generation` arg or raise an error"""
    gen = args.gen
    if not gen:
        raise ValueError(
            "Generation is required! Please pass the generation "
            "using the --gen argument"
        )
    return gen

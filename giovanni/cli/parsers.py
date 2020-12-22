# -*- coding: utf-8 -*-

"""
Configure the argument parsers
"""

import argparse

import giovanni
from giovanni.cli import odds, simulate


def generate_parser():
    """Get the CLI parser

    Configures a parser and attaches subparsers for all CLI commands. Note that
    every new command will require a new subparser. Subparsers are located in
    their own submodule, i.e.::

        odds.py
        simulate.py

    Each submodule should define a `configure_subparser` method which is called
    to add subparser metadata and arguments. Each subparser's namespace tells
    the `do_call` arbitration logic which command is being run.
    """
    p = argparse.ArgumentParser(
        description="giovanni is a tool for simulating shiny encouter rates "
                    "or computing the odds of a shiny encounter"
    )
    p.add_argument(
        "-V", "--version",
        action="version",
        version=f"giovanni {giovanni.__version__}",
        help="Show the giovanni version number and exit.",
    )

    subparsers = p.add_subparsers(
        metavar="commands",
        dest="cmd",
    )
    # http://bugs.python.org/issue9253
    # http://stackoverflow.com/a/18283730/1599393
    subparsers.required = True

    odds.configure_subparser(subparsers)
    simulate.configure_subparser(subparsers)

    return p

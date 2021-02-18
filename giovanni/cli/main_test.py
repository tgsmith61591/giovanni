# -*- coding: utf-8 -*-

from giovanni.cli import main

from unittest import mock


class MockArgs:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


def mock_generate_and_parse(parser, args):
    def _mocked():
        return (parser, args)
    return _mocked


def test_patched_odds():
    with mock.patch(
        "giovanni.cli.parsers.generate_and_parse",
        mock_generate_and_parse(
            None,
            MockArgs(
                cmd="odds",
                verbose=True,
                gen=4,
                soft_resets=1,
                swarm_size=1,
                charm=False,
            ),
        ),
    ):
        ec = main.main()

    assert ec == 0

# -*- coding: utf-8 -*-

import logging
import logging.config

import copy


_default_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(levelname)s] %(asctime)s [%(name)s] - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"]
    }
}


def get_logger(name, level="INFO", config=None):
    """Return a configured logger

    References
    ----------
    .. [1] https://docs.python.org/3/library/logging.html
    """
    if config is None:
        config = copy.deepcopy(_default_logging_config)

        # set the level in the default
        level = level.upper()
        config["handlers"]["console"]["level"] = level
        config["root"]["level"] = level

    logging.config.dictConfig(config)
    return logging.getLogger(name)

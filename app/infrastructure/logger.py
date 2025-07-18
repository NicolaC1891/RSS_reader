"""
This module contains the logger.
"""

import sys
import logging
from logging import StreamHandler, Formatter


def setup_logger(verbose: bool) -> None:
    """
    Switches on/off log messages (default: logs on at DEBUG)
    :param verbose: Bool from CLI params
    :return: None. Sets up the logger
    """
    if not verbose:
        logging.disable(logging.CRITICAL)


def create_logger():
    """
    Creates a logger instance.
    :return: logger instance
    """
    logger = logging.getLogger("__name__")
    logger.setLevel(logging.DEBUG)
    handler = StreamHandler(stream=sys.stdout)
    handler.setFormatter(Formatter(fmt="[%(asctime)s: %(levelname)s] %(message)s"))
    logger.addHandler(handler)
    return logger

logger = create_logger()
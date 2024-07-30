""" . """
import logging
from modulive.utils import catch_exception

logger = logging.getLogger("modulive")


@catch_exception
def handle_reset_key_press(modulive, params, value):
    """Refresh"""
    modulive.broadcast_update()

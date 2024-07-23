"""init modulive"""

from .modulive import Modulive


def create_instance(c_instance):
    """init function called by Ableton"""
    return Modulive(c_instance)

"""init modulive-wootingone"""
from .modulive_wootingone import ModuliveWootingOne


def create_instance(c_instance):
    """init function called by Ableton"""
    return ModuliveWootingOne(c_instance)

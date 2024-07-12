""" init modulive-mft """
from .modulive_mft import ModuliveMFT

def create_instance(c_instance):
    """ init function called by Ableton """
    return ModuliveMFT(c_instance)

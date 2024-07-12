""" Utility functions """
import functools
import traceback
import re
import logging

logger = logging.getLogger("modulive")

def catch_exception(f):
    """ Decorator that logs a traceback from the class in question """
    @functools.wraps(f)
    def func(*args, **kwargs): # pylint: disable=inconsistent-return-statements
        try:
            return f(*args, **kwargs)
        except: # pylint: disable=bare-except
            args[0].log(traceback.format_exc())
    return func

def get_type(s):
    """
    Return substring between arrows of string
    e.g. "<Some_Type>" returns "Some_Type"
    """
    match = re.search(r"(?<=\<)(.*?)(?=\>)",s)
    if match:
        return match.group(0)
    return None

def get_name(s):
    """
    Return substring between braces of string
    e.g. "[Some_Name]" returns "Some_Name"
    """
    match = re.search(r"(?<=\[)(.*?)(?=\])",s)
    if match:
        return match.group(0)
    return None


def get_commands():
    """
    Return a list of all comma separated values between brackets in given string 
    e.g. "{Command1(),Command2()}" returns ["Command1()","Command2()"]
    """

def get_arguments():
    """ 
    Return a list of all comma separated values between parentheses in given string 
    e.g. "(Param1,Param2)" returns ["Param1","Param2"]
    """

def get_children(group_track, all_tracks):
    """ Take a group track and return its child tracks from a list of all tracks

    Args:
        group_track: Ableton Track object
        all_tracks: All tracks in Ableton song
    """
    if not group_track.is_foldable:
        raise TypeError("parameter is not a Group Track")

    children = []
    for track in all_tracks:
        if has_parent(track, group_track):
            children.append(track)
    return children

def has_parent(track, parent):
    """ Recursively move through a tracks parent's to discover if it has a certain ancestor """
    if not track.group_track:
        return False
    if track.group_track == parent:
        return True
    return has_parent(track.group_track, parent)

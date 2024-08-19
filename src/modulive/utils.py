""" Utility functions """
import functools
import traceback
import re
import logging
from threading import Timer

logger = logging.getLogger("modulive")


def catch_exception(f):
    """Decorator that logs a traceback from the class in question"""

    @functools.wraps(f)
    def func(*args, **kwargs):  # pylint: disable=inconsistent-return-statements
        try:
            return f(*args, **kwargs)
        except:  # pylint: disable=bare-except
            logger.error(traceback.format_exc())

    return func


def debounce(wait):
    """Decorator that will postpone a functions
    execution until after wait seconds
    have elapsed since the last time it was invoked."""

    def decorator(fn):
        def debounced(*args, **kwargs):
            def unblock():
                debounced.f = False

            if not hasattr(debounced, "f") or not debounced.f:
                fn(*args, **kwargs)
                debounced.f = True
                debounced.t = Timer(wait, unblock)
                debounced.t.start()

        return debounced

    return decorator


def get_type(s):
    """
    Return substring between arrows of string
    e.g. "<Some_Type>" returns "Some_Type"
    """
    match = re.search(r"(?<=\<)(.*?)(?=\>)", s)
    if match:
        return match.group(0)
    return None


def get_name(s):
    """
    Return substring between braces of string
    e.g. "[Some_Name]" returns "Some_Name"
    """
    match = re.search(r"(?<=\[)(.*?)(?=\])", s)
    if match:
        return match.group(0)
    return None


def get_commands(s):
    """
    Return a list of all comma separated values between brackets in given string
    e.g. "{Command1(),Command2()}" returns ["Command1()","Command2()"]
    """
    match = re.search(r"\{(.*?)\}", s)
    if match:
        return match.group(1).split(",")
    return []


def get_arguments(s):
    """
    Return a list of all comma separated values between parentheses in given string
    e.g. "(Param1,Param2)" returns ["Param1","Param2"]
    """
    match = re.search(r"\((.*?)\)", s)
    if match:
        return match.group(1).split(",")
    return None


def get_param_path(s):
    """
    Return a list of all period separated values
    e.g. "instrument1.param2" returns ["instrument1","param2"]
    """
    return s.split(".")


def get_children(group_track, all_tracks):
    """Take a group track and return its child tracks from a list of all tracks

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
    """Recursively move through a tracks parent's to discover if it has a certain ancestor"""
    if not track.group_track:
        return False
    if track.group_track == parent:
        return True
    return has_parent(track.group_track, parent)


def get_main_device(track):
    """Return the maind device of a track"""
    if len(track.devices) > 0:
        return track.devices[0]
    return None


def get_beats_remaining(song, quantize):
    """Get beats remaining before provided quantize value triggers"""
    beats_remaining = 0
    # if Global, use that quantize
    if quantize == 0:
        quantize = song.clip_trigger_quantization
    else:
        quantize -= 1
    if quantize == 0 or quantize >= 5:
        beats_remaining = 0
    else:
        beat_divisors = {
            1: 8 * song.signature_numerator,
            2: 4 * song.signature_numerator,
            3: 2 * song.signature_numerator,
            4: 1 * song.signature_numerator,
        }
        beat_divisor = beat_divisors[quantize]
        total_beats = song.get_current_beats_song_time().beats + (
            (song.get_current_beats_song_time().bars - 1) * song.signature_numerator
        )
        if total_beats % beat_divisor == 0:
            beats_remaining = 0
        else:
            beats_remaining = beat_divisor - (total_beats % beat_divisor)
    return beats_remaining


def update_parameter_value(param, value):
    """safe update of parameter"""
    if value > param.max:
        value = param.max
    elif value < param.min:
        value = param.min
    param.value = value

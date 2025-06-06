""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception
from modulive_wootingone.constants import Animations

logger = logging.getLogger("modulive")


@catch_exception
def handle_dynamic_key_press(wooting, modulive, params, value):
    """Select/Deselect dynamic clip"""
    xy = params[0]
    idx = int(params[1])
    module = modulive.get_active_module(xy)
    if module:
        if "ctrl" in wooting.get_state()["modifiers"]:
            modulive.unset_active_module(xy)
        elif "shift" in wooting.get_state()["modifiers"]:
            clip = module.get_dynamic_clips()[idx]
            if clip:
                clip.stop()
        elif value > 0:
            clip = module.get_dynamic_clips()[idx]
            if clip:
                clip.select()
        else:
            clip = module.get_dynamic_clips()[idx]
            if clip:
                clip.deselect()


@catch_exception
def handle_dynamic_key_feedback(_, modulive, params, btn, note):
    """Send note to controler to update LED"""
    xy = params[0]
    idx = int(params[1])
    module = modulive.get_active_module(xy)
    if module:
        dc = module.get_dynamic_clips()[idx]
        if dc:
            animation = Animations.DIM
            if dc.get_is_playing():
                animation = Animations.MEDIUM
            if dc.get_is_triggered():
                animation = Animations.FLASHING
            btn.send_midi((MIDI_NOTE_ON_STATUS + animation, note, dc.get_color_index()))
        else:
            btn.send_midi((MIDI_NOTE_ON_STATUS + Animations.DIM, note, 127))

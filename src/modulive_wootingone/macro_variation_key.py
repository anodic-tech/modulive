""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception
from modulive_wootingone.constants import Animations

logger = logging.getLogger("modulive")


@catch_exception
def handle_variation_key_press(_, modulive, params, value):
    """Select/Deselect section"""
    xy = params[0]
    idx = int(params[1])
    module = modulive.get_active_module(xy)
    if module:
        if value > 0:
            module.select_macro_variation(idx)
        else:
            module.deselect_macro_variation(idx)


@catch_exception
def handle_variation_key_feedback(_, modulive, params, btn, note):
    """Send note to controler to update LED"""
    xy = params[0]
    idx = int(params[1])
    module = modulive.get_active_module(xy)
    if module:
        mv = module.get_macro_variation(idx)
        if mv:
            animation = Animations.DIM
            if mv.get_is_active():
                animation = Animations.MEDIUM
            btn.send_midi((MIDI_NOTE_ON_STATUS + animation, note, mv.get_color_index()))
        else:
            btn.send_midi((MIDI_NOTE_ON_STATUS + Animations.DIM, note, 127))
    else:
        btn.send_midi((MIDI_NOTE_ON_STATUS + Animations.DIM, note, 0))

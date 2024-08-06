""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception
from modulive_wootingone.constants import Animations

logger = logging.getLogger("modulive")


@catch_exception
def handle_module_indicator_key_press(wooting, modulive, params, value):
    """If the given active module slot is empty, select a module"""
    xy = params[0]
    if "ctrl" in wooting.get_state()["modifiers"] and value > 0:
        modulive.unset_active_module(xy)
    elif "shift" in wooting.get_state()["modifiers"] and value > 0:
        module = modulive.get_active_module(xy)
        if module:
            module.stop()


@catch_exception
def handle_module_indicator_key_feedback(_, modulive, params, btn, note):
    """Send note to controler to update LED"""
    xy = params[0]
    module = modulive.get_active_module(xy)
    if module:
        btn.send_midi(
            (MIDI_NOTE_ON_STATUS + Animations.MEDIUM, note, module.get_color_index())
        )
    else:
        btn.send_midi((MIDI_NOTE_ON_STATUS + Animations.DIM, note, 0))

""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception
from modulive_wootingone.constants import Animations

logger = logging.getLogger("modulive")


@catch_exception
def handle_module_key_press(wooting, modulive, params, value):
    """If the given active module slot is empty, select a module"""
    xy = params[0]
    idx = int(params[1])
    if "ctrl" in wooting.get_state()["modifiers"]:
        return
    module = modulive.get_module(idx)
    if value > 0 and module and modulive.get_active_module(xy) is None:
        logger.info(f"select MODULE {xy}{idx}")
        modulive.set_active_module(xy, module)


@catch_exception
def handle_module_key_feedback(_, modulive, params, btn, note):
    """Send note to controler to update LED"""
    xy = params[0]
    idx = int(params[1])
    if modulive.get_active_module(xy) is None:
        module = modulive.get_module(idx)
        if module:
            btn.send_midi(
                (
                    MIDI_NOTE_ON_STATUS + Animations.MEDIUM,
                    note,
                    module.get_color_index(),
                )
            )
        else:
            btn.send_midi((MIDI_NOTE_ON_STATUS + Animations.DIM, note, 126))

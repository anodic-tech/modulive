""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception

OUT_CHANNEL = 1

logger = logging.getLogger("modulive")


@catch_exception
def handle_module_key_press(modulive, params, value):
    """If the given active module slot is empty, select a module"""
    ab = params[0]
    idx = int(params[1])
    module = modulive.get_module(idx)
    if value > 0 and module and modulive.get_active_module(ab) is None:
        logger.info(f"select MODULE {ab}{idx}")
        modulive.set_active_module(ab, module)


@catch_exception
def handle_module_key_feedback(modulive, params, btn, note):
    """Send note to controler to update LED"""
    ab = params[0]
    idx = int(params[1])
    if modulive.get_active_module(ab) is None:
        module = modulive.get_module(idx)
        if module:
            btn.send_midi((MIDI_NOTE_ON_STATUS + 2, note, module.get_color_index()))
        else:
            btn.send_midi((MIDI_NOTE_ON_STATUS + 1, note, 0))

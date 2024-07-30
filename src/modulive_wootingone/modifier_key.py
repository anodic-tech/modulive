""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS # type: ignore
from modulive.utils import catch_exception

OUT_CHANNEL = 1

logger = logging.getLogger("modulive")


@catch_exception
def handle_modifier_key_press(wooting, _, params, value):
    """Select/Deselect section"""
    modifier = params[0]
    if value:
        logger.info(f"Enable modifier [{modifier}]")
        wooting.enable_modifier(modifier)
    else:
        logger.info(f"Disable modifier [{modifier}]")
        wooting.disable_modifier(modifier)


@catch_exception
def handle_modifier_key_feedback(wooting, _, params, btn, note):
    """Send note to controler to update LED"""
    modifier = params[0]
    if modifier in wooting.get_state()["modifiers"]:
        btn.send_midi((MIDI_NOTE_ON_STATUS + 2, note, 125))
    else:
        btn.send_midi((MIDI_NOTE_ON_STATUS + 1, note, 125))

""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception
from modulive_wootingone.constants import Animations

logger = logging.getLogger("modulive")


@catch_exception
def handle_global_key_press(wooting, modulive, _, value):
    """."""
    if value:
        if "shift" in wooting.get_state()["modifiers"]:
            modulive.stop_all()


@catch_exception
def handle_global_key_feedback(wooting, _, __, btn, note):
    """Send note to controler to update LED"""
    btn.send_midi((MIDI_NOTE_ON_STATUS + Animations.DIM, note, 125))

""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception
from modulive_wootingone.constants import Animations

logger = logging.getLogger("modulive")


@catch_exception
def handle_section_key_press(wooting, modulive, params, value):
    """Select/Deselect section"""
    ab = params[0]
    idx = int(params[1])
    module = modulive.get_active_module(ab)
    if module:
        if "ctrl" in wooting.get_state()["modifiers"]:
            modulive.unset_active_module(ab)
        elif "shift" in wooting.get_state()["modifiers"]:
            module.stop_section(idx)
        elif value > 0:
            module.select_section(idx)
        else:
            logger.info(f"deselect SECTION {ab}{idx}")


@catch_exception
def handle_section_key_feedback(_, modulive, params, btn, note):
    """Send note to controler to update LED"""
    ab = params[0]
    idx = int(params[1])
    module = modulive.get_active_module(ab)
    if module:
        section = module.get_section(idx)
        if section:
            animation = Animations.DIM
            if section.get_is_playing():
                animation = Animations.MEDIUM
            if section.get_is_triggered():
                animation = Animations.FLASHING
            btn.send_midi(
                (MIDI_NOTE_ON_STATUS + animation, note, section.get_color_index())
            )
        else:
            btn.send_midi((MIDI_NOTE_ON_STATUS + Animations.DIM, note, 127))

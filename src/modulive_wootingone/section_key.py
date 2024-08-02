""" . """
import logging
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception

OUT_CHANNEL = 1

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
            return
        section = module.get_section(idx)
        if section:
            if value > 0:
                section.select()
                logger.info(f"select SECTION {ab}{idx}")
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
            btn.send_midi(
                (MIDI_NOTE_ON_STATUS + OUT_CHANNEL, note, section.get_color_index())
            )
        else:
            btn.send_midi((MIDI_NOTE_ON_STATUS + OUT_CHANNEL, note, 127))

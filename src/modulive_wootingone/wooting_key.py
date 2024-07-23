""" . """
from _Framework.ButtonElement import ButtonElement  # type: ignore
from _Framework.SubjectSlot import subject_slot  # type: ignore
from _Framework.InputControlElement import MIDI_NOTE_TYPE  # type: ignore
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent  # type: ignore
from modulive.utils import catch_exception

IN_CHANNEL = 0
OUT_CHANNEL = 1


class WootingKey(ControlSurfaceComponent):
    """Generic key class"""

    @catch_exception
    def __init__(self, name, note):
        super().__init__()
        self._modulive = self.canonical_parent.modulive
        self._log = self.canonical_parent._log
        self.note = note
        self.btn = ButtonElement(True, MIDI_NOTE_TYPE, IN_CHANNEL, note, name=name)
        self._on_button_value.subject = self.btn

    @subject_slot("value")
    def _on_button_value(self, value):
        """Delegate action once button is triggered"""
        self._handle_action(value)

    def _handle_action(self, _):
        """Default handle action, to be overridden"""

    def handle_state_change(self):
        """Default handle state change, to be overridden"""

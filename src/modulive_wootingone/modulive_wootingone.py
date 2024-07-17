""" . """
from _Framework.ButtonElement import ButtonElement # type: ignore
from _Framework.SubjectSlot import subject_slot_group # type: ignore
from _Framework.InputControlElement import MIDI_NOTE_TYPE # type: ignore
from modulive.modulive_surface import ModuliveSurface
from modulive.utils import catch_exception

KEYS = [
    {
        'name': '2',
        'note': 4,
        'type': 'section'
    }
]

class ModuliveWootingOne(ModuliveSurface):
    """ Modulive - WootingOne Integration """

    @catch_exception
    def __init__(self, *a, **k):
        super().__init__(name="ModuliveWootingOne", *a, **k)
        self.btns = []
        for key in KEYS:
            self.btns.append(ButtonElement(True, MIDI_NOTE_TYPE, 0, key['note'], name=key['name'],
                            send_midi=self._send_midi, register_control=self._register_control ))
        self._log(self.btns)
        self._on_button_value.replace_subjects(self.btns)

    @subject_slot_group('value')
    def _on_button_value(self, value, button):
        """ Delegate action once button is triggered """
        self._handle_action(button.name, value)

    def _handle_action(self, key_name, value):
        """ Handle action based upon controller state, modulive state, and key commands"""
        self._log(key_name)
        self._log(value)

    def _update_mapping(self):
        """ Get params from Modulive """
        self._log(self.modulive.get_state())

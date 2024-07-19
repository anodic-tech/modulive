""" . """
from _Framework.ButtonElement import ButtonElement # type: ignore
from _Framework.SubjectSlot import subject_slot # type: ignore
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_NOTE_ON_STATUS # type: ignore
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # type: ignore
from modulive.modulive_surface import ModuliveSurface
from modulive.utils import catch_exception, get_arguments, get_type

KEYS = [
    {
        'name': '2',
        'note': 4,
        'functions': ['<SECTION_KEY>(A,0)']
    }
]

IN_CHANNEL = 0
OUT_CHANNEL = 1

class ModuliveWootingOne(ModuliveSurface):
    """ Modulive - WootingOne Integration """

    @catch_exception
    def __init__(self, *a, **k):
        super().__init__(name="ModuliveWootingOne", *a, **k)
        with self.component_guard():
            self._key_handlers = []
            for key in KEYS:
                for func in key['functions']:
                    type_name = get_type(func)
                    type_params = get_arguments(func)
                    self._log(type_params)
                    self._key_handlers.append(
                        KEY_TYPES[type_name](key['name'],key['note'],type_params))
            self._log(self._components)

    def _update_mapping(self):
        """ Get params from Modulive """
        self._log(self.modulive.get_state())
        for handler in self._key_handlers:
            handler.handle_state_change()


class WootingKey(ControlSurfaceComponent):
    """ Generic key class """

    @catch_exception
    def __init__(self,name, note):
        super().__init__()
        self._modulive = self.canonical_parent.modulive
        self._log = self.canonical_parent._log
        self.note = note
        self.btn = ButtonElement(True, MIDI_NOTE_TYPE, IN_CHANNEL, note, name=name)
        self._on_button_value.subject = self.btn

    @subject_slot('value')
    def _on_button_value(self, value):
        """ Delegate action once button is triggered """
        self.canonical_parent._log(value)
        self._handle_action(value)

    def _handle_action(self, _):
        """ Default handle action, to be overridden """


class SectionKey(WootingKey):
    """ Section key class """

    @catch_exception
    def __init__(self, name, key, params):
        super().__init__(name, key)
        if len(params) != 2:
            raise TypeError(f'Invalid SectionKey parameters `{params}`')
        self.ab = params[0]
        self.idx = int(params[1])

    @catch_exception
    def _handle_action(self, value):
        """ Called on button press, call actions in Modulive """
        module = self._modulive.active_modules[self.ab]
        if module:
            # section = module.sections[self.idx]
            if value > 0:
                self._log(f'select SECTION {self.ab}{self.idx}')
            else:
                self._log(f'deselect SECTION {self.ab}{self.idx}')
        #TODO: remove and handle state change from modulive
        self.handle_state_change()

    def handle_state_change(self):
        """ Send note to controler to update LED """
        module = self._modulive.active_modules[self.ab]
        if module:
            section = module.sections[self.idx]
            if section:
                self.btn.send_midi(
                    (MIDI_NOTE_ON_STATUS+OUT_CHANNEL, self.note, section.color))

KEY_TYPES = {
    'SECTION_KEY': SectionKey
}

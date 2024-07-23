""" . """
from modulive.utils import catch_exception
from modulive_wootingone.wooting_key import WootingKey

OUT_CHANNEL = 1


class SectionKey(WootingKey):
    """Section key class"""

    @catch_exception
    def __init__(self, name, key, params):
        super().__init__(name, key)
        if len(params) != 2:
            raise TypeError(f"Invalid SectionKey parameters `{params}`")
        self.ab = params[0]
        self.idx = int(params[1])

    @catch_exception
    def _handle_action(self, value):
        """Called on button press, call actions in Modulive"""
        module = self._modulive.active_modules[self.ab]
        if module:
            # section = module.sections[self.idx]
            if value > 0:
                self._log(f"select SECTION {self.ab}{self.idx}")
            else:
                self._log(f"deselect SECTION {self.ab}{self.idx}")

    @catch_exception
    def handle_state_change(self):
        """Send note to controler to update LED"""
        # module = self._modulive.active_modules[self.ab]
        # if module:
        #     section = module.sections[self.idx]
        #     if section:
        #         self.btn.send_midi(
        #             (MIDI_NOTE_ON_STATUS+OUT_CHANNEL, self.note, section.color))
        # elif len(self._modulive.modules) > self.idx + 1:
        #     module = self._modulive.modules[self.idx]
        #     self.btn.send_midi((MIDI_NOTE_ON_STATUS+OUT_CHANNEL, self.note, section.color))

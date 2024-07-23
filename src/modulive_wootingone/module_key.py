""" . """
from _Framework.InputControlElement import MIDI_NOTE_ON_STATUS  # type: ignore
from modulive.utils import catch_exception
from modulive_wootingone.wooting_key import WootingKey


class ModuleKey(WootingKey):
    """Module key class"""

    @catch_exception
    def __init__(self, name, key, params):
        super().__init__(name, key)
        if len(params) != 2:
            raise TypeError(f"Invalid ModuleKey parameters `{params}`")
        self.ab = params[0]
        self.idx = int(params[1])

    @catch_exception
    def _handle_action(self, value):
        """If the given active module slot is empty, select a module"""
        if (
            value > 0
            and len(self._modulive.modules) > self.idx + 1
            and self._modulive.active_modules[self.ab] is None
        ):
            self._log(f"select MODULE {self.ab}{self.idx}")

    @catch_exception
    def handle_state_change(self):
        """Send note to controler to update LED"""
        if self._modulive.active_modules[self.ab] is None:
            module = (
                self._modulive.modules[self.idx]
                if self.idx < len(self._modulive.modules)
                else None
            )
            if module:
                self.btn.send_midi(
                    (MIDI_NOTE_ON_STATUS + 2, self.note, module.get_color_index())
                )
            else:
                self.btn.send_midi((MIDI_NOTE_ON_STATUS + 1, self.note, 0))

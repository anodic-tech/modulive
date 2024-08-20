""" . """
from functools import partial
import Live  # type: ignore
from modulive.modulive_component import ModuliveComponent  # type: ignore
from .utils import catch_exception, get_main_device, update_parameter_value


class VariationKnob(ModuliveComponent):
    """Wrapper for knob on master track that maps to assigned macro variation"""

    def __init__(self):
        super().__init__()

        self._param_map = []
        self._knob = get_main_device(self._song.master_track).parameters[1]
        self._knob.add_value_listener(self._on_knob_value_changed)

        self._is_locked = False
        self._lock_timer = Live.Base.Timer(
            callback=self._unlock, interval=100, repeat=False
        )

        self._assigned_variation = None
        self._reset_knob_flag = False

    def get_knob(self):
        return self._knob

    def _lock(self):
        """prevent updates"""
        self._is_locked = True
        self._lock_timer.stop()
        self._lock_timer.start()

    def _unlock(self):
        """allow updates"""
        self._is_locked = False

    def _reset_knob(self):
        """set knob value back to 0"""
        self._knob.value = self._knob.min
        self._reset_knob_flag = False

    @catch_exception
    def assign_variation(self, macro_variation):
        """set given macro_variation to knob"""
        self._clear_param_map()
        self._assigned_variation = macro_variation
        for param_value in macro_variation.get_param_values():
            param_value["param"].add_value_listener(self._refresh_map)
            p = {
                "param": param_value["param"],
                "starting_value": param_value["param"].value,
                "diff": param_value["target_value"] - param_value["param"].value,
            }
            self._param_map.append(p)

    @catch_exception
    def clear_assignment(self, macro_variation=None):
        """clear macro variation from knob"""
        if macro_variation and macro_variation != self._assigned_variation:
            return
        self._clear_param_map()

    def _clear_param_map(self):
        """reset mapping"""
        self._reset_knob_flag = True
        for param_value in self._param_map:
            if param_value["param"].value_has_listener(self._refresh_map):
                param_value["param"].remove_value_listener(self._refresh_map)
        self._param_map = []
        self._assigned_variation = None
        self._midi_action(self._reset_knob)

    def _refresh_map(self):
        """reassign mapping on external param change"""
        if not self._is_locked:
            self.assign_variation(self._assigned_variation)

    @catch_exception
    def _on_knob_value_changed(self):
        """modify to macro variation as knob reaches 100%"""
        if self._reset_knob_flag:
            return
        self._lock()
        for p in self._param_map:
            new_value = (
                p["starting_value"] + p["diff"] * self._knob.value / self._knob.max
            )
            self._midi_action(partial(update_parameter_value, p["param"], new_value))

    def disconnect(self):
        """clear listeners and timers"""
        self._clear_param_map()
        self._lock_timer.stop()
        self._knob.remove_value_listener(self._on_knob_value_changed)
        super().disconnect()
        return

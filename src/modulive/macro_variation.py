""" . """
from modulive.modulive_component import ModuliveComponent
from .utils import catch_exception, get_main_device, get_name


class MacroVariation(ModuliveComponent):
    """Section component"""

    @catch_exception
    def __init__(
        self,
        config_clip,
        track_clips,
    ):
        super().__init__()
        self._config_clip = config_clip
        self._track_clips = track_clips
        self._active = False
        self._value = 0
        self._log(f'Creating Macro Variation {self.get_name()}...')

    def get_name(self):
        """Get variation name"""
        return get_name(self._config_clip.name)

    def get_color_index(self):
        """Get variation color index"""
        return self._config_clip.color_index

    def get_is_active(self):
        return self._active

    def get_value(self):
        return self._value

    def get_state(self):
        """Return a dict representation of object state"""
        return {
            "name": self.get_name(),
            "color_index": self.get_color_index(),
            "is_active": self.get_is_active(),
            "value": self.get_value(),
        }

    def get_param_values(self):
        param_values = []
        for track_clip in self._track_clips:
            device = get_main_device(track_clip[0])
            for param in device.parameters:
                envelope = track_clip[1].automation_envelope(param)
                if envelope:
                    param_values.append(
                        {"param": param, "target_value": envelope.value_at_time(0.1)}
                    )
        return param_values

    def select(self):
        self._active = True
        # self.modulive.assign_variation_knob(self)
        self.ramp()
        self._broadcast_update()

    def deselect(self):
        self._active = False
        self.modulive.clear_variation_knob(self)
        self._broadcast_update()

    def ramp(self, quantization=0):
        for param_value in self.get_param_values():
            self.modulive.ramp_param(
                param_value["param"], param_value["target_value"], quantization
            )

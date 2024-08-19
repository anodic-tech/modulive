""" . """
import Live  # type: ignore
from modulive.modulive_component import ModuliveComponent  # type: ignore
from .utils import catch_exception, get_beats_remaining, update_parameter_value


class ParamRamper(ModuliveComponent):
    """Scheduler for ramping parameters"""

    @catch_exception
    def __init__(self):
        super().__init__()

        self._scheduler = Live.Base.Timer(
            callback=self.on_tick, interval=1, repeat=True
        )
        self._scheduler.start()
        self._ramping_params = []

        self._last_beat = self._song.get_current_beats_song_time().beats
        self._last_subdivision = self._song.get_current_beats_song_time().sub_division
        self._last_tick = self._song.get_current_beats_song_time().ticks

    @catch_exception
    def ramp_param(self, param, value, quantization):
        """ramp given param to value before quantization hits"""

        num_beats = get_beats_remaining(self._song, quantization)

        for ramping_param in self._ramping_params:
            if ramping_param["param"] == param:
                self._ramping_params.remove(ramping_param)

        if not self._song.is_playing:
            param.value = value
            return

        self._ramping_params.append(
            {"param": param, "beats_remaining": num_beats, "target_value": value}
        )

    @catch_exception
    def on_tick(self):
        """ramp params on each tick"""
        if len(self._ramping_params) > 0:
            self._do_ramp()
            self._last_beat = self._song.get_current_beats_song_time().beats
            self._last_subdivision = (
                self._song.get_current_beats_song_time().sub_division
            )
            self._last_tick = self._song.get_current_beats_song_time().ticks

    @catch_exception
    def _do_ramp(self):
        """execute ramp"""
        current_tick = self._song.get_current_beats_song_time().ticks
        tick_difference = float(current_tick - self._last_tick)

        if tick_difference < 0:
            tick_difference += 60

        for param in self._ramping_params:
            ticks_remaining = float(
                param["beats_remaining"] * 4 * 60
                + (4 - self._last_subdivision) * 60
                + 60
                - self._last_tick
            )
            if ticks_remaining <= 0:
                update_parameter_value(param["param"], param["target_value"])
                self._ramping_params.remove(param)
                return
            elif ticks_remaining < 100:
                value_difference = float(param["target_value"] - param["param"].value)
                new_value = (
                    tick_difference / ticks_remaining * value_difference
                    + param["param"].value
                )
                update_parameter_value(param["param"], new_value)

            if self._song.get_current_beats_song_time().beats != self._last_beat:
                param["beats_remaining"] -= 1

    @catch_exception
    def disconnect(self):
        """Cleanup. Nonmutative."""
        self._scheduler.stop()
        super().disconnect()

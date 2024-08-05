""" . """
from __future__ import with_statement
import math
from functools import partial
import Live  # type: ignore
from _Framework.EncoderElement import EncoderElement  # type: ignore
from modulive.modulive_surface import ModuliveSurface
from modulive.utils import catch_exception

MIDI_CC_TYPE = 1
MIDI_ROTARY_CHANNEL = 0
MIDI_SWITCH_CHANNEL = 1
ENCODER_COUNT = 16

color_index_map = {
    0: 0,
    9: 1,  # blue
    12: 95,  # pink
    39: 105,  # lavender
    56: 90,  # red
    61: 50,  # green
    69: 90,  # white
    13: 90,  # white
    59: 67,  # gold,
    1: 75,  # orange
    20: 30,  # teal
    24: 115,  # purple
    55: 90,  # white
}


class ModuliveMFT(ModuliveSurface):
    """Modulive - MIDI Fighter Twister Integration"""

    @catch_exception
    def __init__(self, *a, **k):
        super().__init__(name="ModuliveMFT", *a, **k)
        self.listeners = [None] * ENCODER_COUNT
        self.encoders = [None] * ENCODER_COUNT
        self.buttons = [None] * ENCODER_COUNT
        self.params = [None] * ENCODER_COUNT

        with self.component_guard():
            i = 0
            while i < ENCODER_COUNT:
                self.encoders[i] = EncoderElement(
                    MIDI_CC_TYPE, MIDI_ROTARY_CHANNEL, i, Live.MidiMap.MapMode.absolute
                )
                self.buttons[i] = EncoderElement(
                    MIDI_CC_TYPE, MIDI_SWITCH_CHANNEL, i, Live.MidiMap.MapMode.absolute
                )
                self.buttons[i].add_value_listener(
                    partial(self._on_midi_button_trigger, i)
                )
                i += 1

            # Assign Crossfader
            crossfader = self.song().master_track.mixer_device.crossfader
            self._assign_encoder(13, crossfader, 55)

    def _update_mapping(self):
        """Get params from Modulive"""
        self._log(self.modulive.get_active_params("A"))

    def _assign_encoder(self, n, param, color=None):
        """Assign an encoder to a parameter"""
        # if previously assigned remove mapping
        if self.listeners[n]:
            self.listeners[n]()

        # add listener to param
        update_encoder = partial(self._update_encoder, n, param)
        param.add_value_listener(update_encoder)

        # add listener to encoder
        self.params[n] = param
        update_param = partial(self._update_param, n)
        self.encoders[n].add_value_listener(update_param)

        # add a way to remove mapping
        self.listeners[n] = partial(
            self._remove_listener, param, self.encoders[n], update_encoder, update_param
        )

        # set encoder color based on name
        if color is not None:
            rgb = color_index_map[color]
            self._send_midi((177, n, rgb))
            self._send_midi((178, n, 47))
        else:
            self._send_midi((178, n, 17))
            self._send_midi((176, n, 0))

        update_encoder()

    def _update_encoder(self, index, param):
        """Update an encoder with parameter value"""
        value = math.floor((param.value - param.min) / (param.max - param.min) * 127)
        self._send_midi((176, index, value))

    def _update_param(self, index, encoder_value):
        """Update a param with encoder value"""
        param = self.params[index]
        value = (encoder_value / 127) * (param.max - param.min) + param.min
        param.value = value

    def _on_midi_button_trigger(self, i, _):
        """Reenable automation on a param on press"""
        if self.params[i]:
            self.params[i].re_enable_automation()

    def _remove_listener(self, param, encoder, update_encoder, update_param):
        if param.value_has_listener(update_encoder):
            param.remove_value_listener(update_encoder)
        if encoder.value_has_listener(update_param):
            encoder.remove_value_listener(update_param)
        if param in self.params:
            self.params[self.params.index(param)] = None

    def _clear_encoder(self, index):
        self._send_midi((178, index, 17))
        self._send_midi((176, index, 0))
        if self.listeners[index]:
            self.listeners[index]()
            self.listeners[index] = None
            self.params[index] = None

    def _rebuild(self):
        i = 0
        while i < ENCODER_COUNT:
            self._clear_encoder(i)
            i += 1

    # def switch_bank(self, bank):
    #     self._send_midi((147,bank,127))

    def disconnect(self):
        """."""
        self._rebuild()
        super().disconnect()

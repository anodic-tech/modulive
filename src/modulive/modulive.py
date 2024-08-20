""" . """
import os
import logging
from collections import deque
from _Framework.ControlSurface import ControlSurface  # type: ignore
from _Framework.ButtonElement import ButtonElement  # type: ignore
from _Framework.InputControlElement import MIDI_NOTE_TYPE, MIDI_NOTE_ON_STATUS # type: ignore
from modulive.param_ramper import ParamRamper
from modulive.variation_knob import VariationKnob  # type: ignore
from .utils import catch_exception, debounce, get_main_device, get_type
from .constants import Types
from .socket import Socket
from .module import Module

logger = logging.getLogger("modulive")


class Modulive(ControlSurface):
    """The entry point to the control surface script. Defines available actions."""

    IS_MODULIVE = True
    MIDI_QUEUE_SIZE = 64

    @catch_exception
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._start_logging()

        self._log("Initializing Modulive...")

        self._modules = []
        self._active_modules = {"X": None, "Y": None}

        self._mapping_listeners = []

        self._can_modify_tempo = False

        with self.component_guard():
            self._socket = Socket()
            self._create_midi_buttons()
            self._param_ramper = ParamRamper()
            self._variation_knob = VariationKnob()
            self._build_tree()
            self.song().add_tracks_listener(self.rebuild_tree)

    # Build

    def _build_tree(self):
        """Iterate through tracks and build virtual tree. Nonmutative"""
        for track in self.song().tracks:
            if get_type(track.name) is Types.MODULE:
                self._modules.append(Module(track))
        self.schedule_message(1, self.broadcast_update)

    @catch_exception
    def rebuild_tree(self):
        """Disconnect modules and rebuild virtual tree. Nonmutative."""
        for m in self._modules:
            m.disconnect()
        self._modules = []
        self._build_tree()

    # Getters

    def get_state(self):
        """Returns a dictionary representation of the application state"""
        return {
            "modules": list(
                map(
                    lambda m: m.get_state(),
                    self._modules,
                )
            ),
            "active_module": {
                "X": self._active_modules["X"].get_active_state()
                if self._active_modules["X"]
                else None,
                "Y": self._active_modules["Y"].get_active_state()
                if self._active_modules["Y"]
                else None,
            },
            "xfade": self.song().master_track.mixer_device.crossfader.value,
            "variation_knob": get_main_device(self.song().master_track)
            .parameters[1]
            .value,
            "tempo": self.song().tempo
        }

    def get_active_params(self, xy):
        """Return a list of active Ableton Parameters for module X or Y"""
        return [1, 2, 3]

    def get_active_module(self, xy):
        """Return active module, X/Y"""
        return self._active_modules[xy]

    def get_module(self, idx):
        """Return module of given index"""
        if len(self._modules) <= idx:
            return None
        return self._modules[idx]
    
    def get_dynamic_param(self):
        """Return macro_variation knob or bpm knob"""
        if self._can_modify_tempo:
            self._log(get_main_device(self.song().master_track).parameters[2].name)
            return [get_main_device(self.song().master_track).parameters[2], 61]
        else:
            return [self._variation_knob.get_knob(), 59, 0, 127]

    # Actions

    @catch_exception
    def set_active_module(self, xy, module):
        """Set active module"""
        if (
            self._active_modules["X"] is not module
            and self._active_modules["Y"] is not module
        ):
            module.activate(xy)
            self._active_modules[xy] = module
            self.broadcast_update()

    @catch_exception
    def unset_active_module(self, xy):
        """Unset active module"""
        xfade = self.song().master_track.mixer_device.crossfader
        if (
            xy == "X"
            and xfade.value < xfade.max
            or xy == "Y"
            and xfade.value > xfade.min
        ):
            self.show_message(
                "Crossfader must be fully transitioned before unsetting module."
            )
            return
        self._active_modules[xy].deactivate()
        self._active_modules[xy] = None
        self.broadcast_update()

    @catch_exception
    def stop_all(self):
        """Stop all playing clips"""
        self.song().stop_all_clips()

    @catch_exception
    def _create_midi_buttons(self):
        """Instantiate array of buttons to receive internal midi calls"""
        self._midi_actions = deque()
        self._midi_buttons = [None] * self.MIDI_QUEUE_SIZE
        self._current_midi_button = 0
        i = 0
        while i < self.MIDI_QUEUE_SIZE:
            self._midi_buttons[i] = ButtonElement(
                True, MIDI_NOTE_TYPE, 15, i, name="global_button"
            )
            self._midi_buttons[i].add_value_listener(self._on_midi_button_trigger)
            i += 1

    def trigger_midi_action(self, action, priority):
        """Add a function call to a queue of midi actions
        to be called upon receiving internal midi"""
        if priority:
            self._midi_actions.append(action)
        else:
            self._midi_actions.appendleft(action)
        self._send_midi((MIDI_NOTE_ON_STATUS + 15, self._current_midi_button, 127))
        self._current_midi_button += 1
        if self._current_midi_button >= self.MIDI_QUEUE_SIZE:
            self._current_midi_button = 0

    def _on_midi_button_trigger(self, _):
        """Trigger intenal midi action"""
        action = self._midi_actions.pop()
        action()

    @catch_exception
    def ramp_param(self, param, value, quantization):
        self._param_ramper.ramp_param(param, value, quantization)

    @catch_exception
    def assign_variation_knob(self, macro_variation):
        self._variation_knob.assign_variation(macro_variation)

    @catch_exception
    def clear_variation_knob(self, macro_variation):
        self._variation_knob.clear_assignment(macro_variation)

    @catch_exception
    def toggle_tempo_modification(self,show):
        """Allow or disallow tempo modifcation"""
        self._can_modify_tempo = show 
        self.broadcast_update()

    # Updates
    @debounce(0.01)
    def broadcast_update(self):
        """Let all listeners know the state has updated"""
        self._socket.send("message", self.get_state())
        for callback in self._mapping_listeners:
            callback()

    def add_mapping_listener(self, callback):
        """Add a callback function to _mapping_listeners"""
        self._mapping_listeners.append(callback)

    def remove_mapping_listener(self, callback):
        """Remove a callback function to _mapping_listeners"""
        self._mapping_listeners.remove(callback)

    # Logging

    def _start_logging(self):
        """If a local log doesn't exist create one.
        Wipe the log clean. Add associated file handler to the logger."""
        module_path = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(module_path, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir, 0o755)
        log_path = os.path.join(log_dir, "modulive.log")
        open(  # pylint: disable=consider-using-with,unspecified-encoding
            log_path, "w"
        ).close()
        self.log_file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter("(%(asctime)s) [%(levelname)s] %(message)s")
        self.log_file_handler.setFormatter(formatter)
        logger.addHandler(self.log_file_handler)

    def _log(self, message):
        """Log locally and to Ableton Log.txt"""
        logger.info(message)

    @catch_exception
    def disconnect(self):
        """Cleanup. Nonmutative."""
        self._log("Disconnecting Modulive...")
        if self.song().tracks_has_listener(self.rebuild_tree):
            self.song().remove_tracks_listener(self.rebuild_tree)
        super().disconnect()
        logger.removeHandler(self.log_file_handler)

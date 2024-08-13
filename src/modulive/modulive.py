""" . """
import os
import logging
from _Framework.ControlSurface import ControlSurface  # type: ignore
from .utils import catch_exception, debounce, get_type
from .constants import Types
from .socket import Socket
from .module import Module

logger = logging.getLogger("modulive")


class Modulive(ControlSurface):
    """The entry point to the control surface script. Defines available actions."""

    IS_MODULIVE = True

    @catch_exception
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._start_logging()

        self._log("Initializing Modulive...")

        self._modules = []
        self._active_modules = {"X": None, "Y": None}

        self._mapping_listeners = []

        with self.component_guard():
            self._socket = Socket()
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

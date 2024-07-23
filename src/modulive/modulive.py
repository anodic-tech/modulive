""" . """
import os
import logging
from _Framework.ControlSurface import ControlSurface  # type: ignore
from .utils import catch_exception, get_type
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

        self.modules = []
        self.active_modules = {"A": None, "B": None}

        self._mapping_listeners = []

        with self.component_guard():
            self._socket = Socket()
            self._build_tree()
            self.song().add_tracks_listener(self.rebuild_tree)

    def _build_tree(self):
        """Iterate through tracks and build virtual tree"""
        for track in self.song().tracks:
            if get_type(track.name) is Types.MODULE:
                self.modules.append(Module(track))
        self.broadcast_update()

    @catch_exception
    def rebuild_tree(self):
        """Disconnect modules and rebuild virtual tree"""
        for m in self.modules:
            m.disconnect()
        self.modules = []
        self._build_tree()

    def get_state(self):
        """Returns a dictionary representation of the application state"""
        return {
            "modules": list(
                map(
                    lambda m: {"name": m.get_name(), "color": m.get_color_index()},
                    self.modules,
                )
            )
        }

    def get_active_params(self, active_module):
        """Return a list of active Ableton Parameters for module A or B"""
        self._log(active_module)
        return [1, 2, 3]

    def broadcast_update(self):
        """Let all listeners know the state has updated"""
        self._log("state update")
        self._socket.send("message", self.get_state())
        for callback in self._mapping_listeners:
            callback()

    def add_mapping_listener(self, callback):
        """Add a callback function to _mapping_listeners"""
        self._mapping_listeners.append(callback)

    def remove_mapping_listener(self, callback):
        """Remove a callback function to _mapping_listeners"""
        self._mapping_listeners.remove(callback)

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
        """Cleanup"""
        self._log("Disconnecting Modulive...")
        if self.song().tracks_has_listener(self.rebuild_tree):
            self.song().remove_tracks_listener(self.rebuild_tree)
        super().disconnect()
        logger.removeHandler(self.log_file_handler)

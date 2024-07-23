""" . """
import logging
from _Framework.ControlSurface import ControlSurface  # type: ignore
from .utils import catch_exception

logger = logging.getLogger("modulive")


class ModuliveSurface(ControlSurface):
    """Generic ControlSurface for integration with MIDI controllers"""

    @catch_exception
    def __init__(self, *a, name="", **k):
        super().__init__(*a, **k)
        self.name = name
        self._log(f"Connecting {self.name}...")

        self.modulive = None
        for control_surface in self._control_surfaces():
            if hasattr(control_surface, "IS_MODULIVE"):
                self.modulive = control_surface
        if not self.modulive:
            raise ImportError("Modulive ControlSurface not found")

        self.modulive.add_mapping_listener(self._update_mapping)

    def _update_mapping(self):
        """To be extended"""
        self._log(self.modulive.get_state())

    def _log(self, message):
        """Log locally and to Ableton Log.txt"""
        logger.info(message)

    @catch_exception
    def disconnect(self):
        """Cleanup"""
        self._log(f"Disconnecting {self.name}...")
        if self.modulive:
            self.modulive.remove_mapping_listener(self._update_mapping)
        super().disconnect()

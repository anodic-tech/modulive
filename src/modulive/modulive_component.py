""" . """
import logging
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent  # type: ignore

logger = logging.getLogger("modulive")


class ModuliveComponent(
    ControlSurfaceComponent
):  # pylint: disable=too-few-public-methods
    """Extendable component providing Modulive specific methods."""

    def __init__(self):
        super().__init__()
        self._listener_removers = []

    def _log(self, message):
        """Call log"""
        logger.info(message)

    def _error(self, message):
        """Call error"""
        logger.error(message)

    def _broadcast_update(self):
        """Notify listeners of state update"""
        self.canonical_parent.broadcast_update()

    def _midi_action(self, action, priority=False):
        """Call a deffered action"""
        self.canonical_parent.trigger_midi_action(action, priority)

    def _add_listener(self, add, exists, remove, callback):
        """Add a listener function that will be removed on disconnect"""
        add(callback)

        def remover():
            if exists(callback):
                remove(callback)

        self._listener_removers.append(remover)

    def disconnect(self):
        """."""
        for listener_remover in self._listener_removers:
            listener_remover()
        super().disconnect()

""" . """
import logging
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # type: ignore

logger = logging.getLogger("modulive")

class ModuliveComponent(ControlSurfaceComponent): # pylint: disable=too-few-public-methods
    """ Extendable component providing Modulive specific methods."""

    def _log(self, message):
        """ Call log """
        logger.info(message)

    def _error(self, message):
        """ Call error """
        logger.error(message)

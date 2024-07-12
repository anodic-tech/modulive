""" . """
import logging
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # type: ignore

logger = logging.getLogger("modulive")

class ModuliveComponent(ControlSurfaceComponent):
    """ Extendable component providing Modulive specific methods."""

    def log(self, message):
        """ Call log via Modulive ControlSurface """
        logger.info(message)

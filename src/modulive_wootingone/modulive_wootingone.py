""" . """
import logging
from _Framework.ControlSurface import ControlSurface # type: ignore

logger = logging.getLogger("modulive")

class ModuliveWootingOne(ControlSurface):
    """ The entry point to the control surface script. Defines available actions. """

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        logger.info("Initializing Modulive-WootingOne Integration...")

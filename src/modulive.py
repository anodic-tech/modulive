""" ControlSurface script container """

import os
import logging
from _Framework.ControlSurface import ControlSurface # type: ignore

logger = logging.getLogger("modulive")

class Modulive(ControlSurface):
    """ The entry point to the control surface script. Defines available actions. """

    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.start_logging()
        self.log("Initializing Modulive...")

    def start_logging(self):
        """ If a local log doesn't exist create one. 
        Wipe the log clean. Add associated file handler to the logger. """
        module_path = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(module_path, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir, 0o755)
        log_path = os.path.join(log_dir, "modulive.log")
        open(log_path, 'w').close()
        self.log_file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter("(%(asctime)s) [%(levelname)s] %(message)s")
        self.log_file_handler.setFormatter(formatter)
        logger.addHandler(self.log_file_handler)

    def disconnect(self):
        """ Cleanup """
        self.log("Disconnecting Modulive...")
        logger.removeHandler(self.log_file_handler)
        super().disconnect()

    def log(self, message):
        """ Log locally and to Ableton Log.txt """
        logger.info(message)

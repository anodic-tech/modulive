""" . """
import os
import logging
from _Framework.ControlSurface import ControlSurface # type: ignore
from .utils import catch_exception, get_type
from .constants import Types
from .socket import Socket
from .module import Module

logger = logging.getLogger("modulive")

class Modulive(ControlSurface):
    """ The entry point to the control surface script. Defines available actions. """

    @catch_exception
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self.start_logging()

        self.log("Initializing Modulive...")

        self._modules = []

        with self.component_guard():
            self._register_component(Socket())
            self._build()


    def _build(self):
        """ Iterate through tracks and build Module components """
        for track in self.song().tracks:
            if get_type(track.name) is Types.MODULE:
                module = Module(track)
                self._register_component(module)
                self._modules.append(module)

    def get_state(self):
        """ Returns a dictionary representation of the application state """
        return {
            'modules': list(map(lambda m: m.name, self._modules))
        }

    def start_logging(self):
        """ If a local log doesn't exist create one. 
        Wipe the log clean. Add associated file handler to the logger. """
        module_path = os.path.dirname(os.path.realpath(__file__))
        log_dir = os.path.join(module_path, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir, 0o755)
        log_path = os.path.join(log_dir, "modulive.log")
        open(log_path, 'w').close() # pylint: disable=consider-using-with,unspecified-encoding
        self.log_file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter("(%(asctime)s) [%(levelname)s] %(message)s")
        self.log_file_handler.setFormatter(formatter)
        logger.addHandler(self.log_file_handler)

    def log(self, message):
        """ Log locally and to Ableton Log.txt """
        logger.info(message)

    def disconnect(self):
        """ Cleanup """
        self.log("Disconnecting Modulive...")
        super().disconnect()
        logger.removeHandler(self.log_file_handler)

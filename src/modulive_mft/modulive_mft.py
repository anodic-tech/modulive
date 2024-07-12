""" . """
from modulive.modulive_surface import ModuliveSurface

class ModuliveMFT(ModuliveSurface):
    """ Modulive - MIDI Fighter Twister Integration """

    def __init__(self, *a, **k):
        super().__init__(name="ModuliveMFT", *a, **k)

    def _update_mapping(self):
        """ Get params from Modulive """
        self._log(self.modulive.get_active_params('A'))

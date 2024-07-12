""" . """
from modulive.modulive_surface import ModuliveSurface

class ModuliveWootingOne(ModuliveSurface):
    """ Modulive - WootingOne Integration """

    def __init__(self, *a, **k):
        super().__init__(name="ModuliveWootingOne", *a, **k)

    def _update_mapping(self):
        """ Get params from Modulive """
        self._log(self.modulive.get_state())

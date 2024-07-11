""" . """
from _Framework.ControlSurfaceComponent import ControlSurfaceComponent # type: ignore

class ModuliveComponent(ControlSurfaceComponent):
    """ Extendable component providing Modulive specific methods."""

    def log(self, message):
        """ Call log via Modulive ControlSurface """
        self.canonical_parent.log(message)

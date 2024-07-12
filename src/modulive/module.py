""" . """
from .utils import catch_exception, get_children, get_name
from .modulive_component import ModuliveComponent

class Module(ModuliveComponent):
    """ Module component """

    @catch_exception
    def __init__(self, track):
        super().__init__()

        self.name = get_name(track.name)
        self._log(f"Creating Module [{self.name}]...")

        self._tracks = get_children(track, self.canonical_parent.song().tracks)
        self._log(f'Tracks: {list(map(lambda t: t.name, self._tracks))}')

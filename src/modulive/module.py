""" . """
from .utils import catch_exception, get_children, get_name
from .modulive_component import ModuliveComponent
from .section import Section


class Module(ModuliveComponent):
    """Module component"""

    @catch_exception
    def __init__(self, track):
        super().__init__()

        self._track = track
        self._log(f"Creating Module [{self.get_name()}]...")

        self._child_tracks = get_children(track, self.canonical_parent.song().tracks)
        self._log(f"Tracks: {list(map(lambda t: t.name, self._child_tracks))}")

        self._sections = []

        self._add_name_and_color_listeners()

    def get_name(self):
        """Get main track name"""
        return get_name(self._track.name)

    def get_color_index(self):
        """Get track color index"""
        return self._track.color_index

    def get_section(self, idx):
        """Get section with index"""
        if len(self._sections) <= idx:
            return None
        return self._sections[idx]

    def activate(self):
        """Prepare module for performance"""
        self._log(f"Activating Module [{self.get_name()}]...")

    def deactivate(self):
        """Disable module"""
        self._log(f"Dectivating Module [{self.get_name()}]...")

    def _add_name_and_color_listeners(self):
        """Broadcast state change on color or name update"""
        for track in [self._track] + self._child_tracks:
            track.add_name_listener(self._broadcast_update)
            track.add_color_index_listener(self._broadcast_update)

    @catch_exception
    def disconnect(self):
        """Remove all listeners and disconnect"""
        for track in [self._track] + self._child_tracks:
            if track.name_has_listener(self._broadcast_update):
                track.remove_name_listener(self._broadcast_update)
            if track.color_index_has_listener(self._broadcast_update):
                track.remove_color_index_listener(self._broadcast_update)
        super().disconnect()

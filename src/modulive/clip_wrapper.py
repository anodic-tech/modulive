""" . """
from .utils import catch_exception, get_name
from .modulive_component import ModuliveComponent


class ClipWrapper(ModuliveComponent):
    """ClipWrapper component"""

    @catch_exception
    def __init__(self, clip, track):
        super().__init__()

        self._clip = clip
        self._track = track

        self._add_listeners()

    def get_name(self):
        """Get main track name"""
        return get_name(self._clip.name)

    def get_color_index(self):
        """Get track color index"""
        return self._clip.color_index

    def get_is_playing(self):
        """Return true if clip is playing"""
        return self._clip.is_playing

    def get_is_triggered(self):
        """Return true if clip is triggered"""
        return self._clip.is_triggered

    def select(self):
        """Calls clip's select action"""
        self._clip.fire()

    def stop(self):
        """Calls clip's select action"""
        self._clip.stop()

    def _add_listeners(self):
        """Broadcast state change on color or name update"""
        self._clip.add_name_listener(self._broadcast_update)
        self._clip.add_color_index_listener(self._broadcast_update)
        self._clip.add_playing_status_listener(self._broadcast_update)

    @catch_exception
    def disconnect(self):
        """Remove all listeners and disconnect"""
        if self._clip.name_has_listener(self._broadcast_update):
            self._clip.remove_name_listener(self._broadcast_update)
        if self._clip.color_index_has_listener(self._broadcast_update):
            self._clip.remove_color_index_listener(self._broadcast_update)
        if self._clip.playing_status_has_listener(self._broadcast_update):
            self._clip.remove_playing_status_listener(self._broadcast_update)
        super().disconnect()

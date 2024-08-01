""" . """
from .utils import catch_exception, get_name
from .modulive_component import ModuliveComponent


class Section(ModuliveComponent):
    """Section component"""

    @catch_exception
    def __init__(self, config_clip, clips):
        super().__init__()
        self._config_clip = config_clip
        self._clips = clips

        # self._log(f"Creating Section [{self.get_name()}]...")

        self._add_name_and_color_listeners()

    def get_name(self):
        """Get main track name"""
        return get_name(self._config_clip.name)

    def get_color_index(self):
        """Get track color index"""
        return self._config_clip.color_index

    def _add_name_and_color_listeners(self):
        """Broadcast state change on color or name update"""
        for clip in self._clips:
            clip.add_name_listener(self._broadcast_update)
            clip.add_color_index_listener(self._broadcast_update)

    @catch_exception
    def disconnect(self):
        """Remove all listeners and disconnect"""
        for clip in self._clips:
            if clip.name_has_listener(self._broadcast_update):
                clip.remove_name_listener(self._broadcast_update)
            if clip.color_index_has_listener(self._broadcast_update):
                clip.remove_color_index_listener(self._broadcast_update)
        super().disconnect()

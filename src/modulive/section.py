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

    def get_name(self):
        """Get main track name"""
        return get_name(self._config_clip.name)

    def get_color_index(self):
        """Get track color index"""
        return self._config_clip.color_index

    def get_is_playing(self):
        """Return true if a clip is playing"""
        for clip in self._clips:
            if clip.get_is_playing():
                return True
        return False

    def get_is_triggered(self):
        """Return true if a clip is triggered"""
        for clip in self._clips:
            if clip.get_is_triggered():
                return True
        return False

    def select(self):
        """Select all clips in section"""
        for clip in self._clips:
            clip.select()

    def stop(self):
        """Stop all clips in section"""
        for clip in self._clips:
            clip.stop()

    @catch_exception
    def disconnect(self):
        """Remove all listeners and disconnect"""
        super().disconnect()

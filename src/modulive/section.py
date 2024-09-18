""" . """
from modulive.scene import Scene
from .utils import catch_exception, get_arguments


class Section(Scene):
    """Section component"""

    @catch_exception
    def __init__(self, config_clip, clips):
        super().__init__(config_clip, clips)
        self._log(f"Creating Section [{self.get_name()}]...")

    # Get

    @catch_exception
    def get_mapping(self):
        """Get the mapping name for this section"""
        if len(self._config_clip.name) > 0:
            return get_arguments(self._config_clip.name)[0]
        return None

    @catch_exception
    def get_macro_variation_names(self):
        """Get the macro variation for this section"""
        if len(get_arguments(self._config_clip.name)) > 1:
            return get_arguments(self._config_clip.name)[1:]
        return []

    def get_clip_for_track(self, track):
        """Get clip for given track"""
        for clip in self._clips:
            if clip.get_track() == track:
                return clip
        return False

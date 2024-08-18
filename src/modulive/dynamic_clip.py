""" . """
from modulive.scene import Scene
from .utils import catch_exception


class DynamicClip(Scene):
    """Dynamic Clip component"""

    @catch_exception
    def __init__(self, config_clip, clips):
        super().__init__(config_clip, clips)

    def select(self):
        """Select all clips in dynamic clip"""
        for clip in self._clips:
            if clip._clip != self._config_clip:
                clip.select()

    def deselect(self):
        """deSelect all clips in dynamic clip"""
        for clip in self._clips:
            if clip._clip != self._config_clip:
                clip.deselect()

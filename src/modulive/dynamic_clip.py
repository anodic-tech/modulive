""" . """
from modulive.scene import Scene
from .utils import catch_exception


class DynamicClip(Scene):
    """Dynamic Clip component"""

    @catch_exception
    def __init__(self, config_clip, clips):
        super().__init__(config_clip, clips)

""" . """
from modulive.scene import Scene
from .utils import catch_exception, get_arguments


class Section(Scene):
    """Section component"""

    @catch_exception
    def __init__(self, config_clip, clips):
        super().__init__(config_clip, clips)
        # self._log(f"Creating Section [{self.get_name()}]...")

    # Get

    @catch_exception
    def get_mapping(self):
        """Get the mapping name for this section"""
        return get_arguments(self._config_clip.name)[0]

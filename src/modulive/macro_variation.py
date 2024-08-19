""" . """
from modulive.modulive_component import ModuliveComponent
from .utils import catch_exception, get_name

class MacroVariation(ModuliveComponent):
    """Section component"""

    @catch_exception
    def __init__(self, config_clip, clips):
        super().__init__()
        self._config_clip = config_clip
        self._clips = clips
        self._active = False

    def get_name(self):
        """Get variation name"""
        return get_name(self._config_clip.name)

    def get_color_index(self):
        """Get variation color index"""
        return self._config_clip.color_index
    
    def get_is_active(self):
        return self._active
    
    def get_value(self):
        return 0
    
    def get_state(self):
        """Return a dict representation of object state"""
        return {
            "name": self.get_name(),
            "color_index": self.get_color_index(),
            "is_active": self.get_is_active(),
            "value": self.get_value()
        }
    
    def select(self):
        self._active = True
        self._broadcast_update()

    def deselect(self):
        self._active = False
        self._broadcast_update()

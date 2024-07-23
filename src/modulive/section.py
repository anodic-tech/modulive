""" . """
from .utils import catch_exception
from .modulive_component import ModuliveComponent


class Section(ModuliveComponent):
    """Section component"""

    @catch_exception
    def __init__(self):
        super().__init__()
        self.color = 61

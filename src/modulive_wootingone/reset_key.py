""" . """
from modulive.utils import catch_exception
from modulive_wootingone.wooting_key import WootingKey


class ResetKey(WootingKey):
    """Reset key class"""

    @catch_exception
    def __init__(self, name, key, _):
        super().__init__(name, key)

    @catch_exception
    def _handle_action(self, _):
        """Refresh"""
        self.canonical_parent.refresh_state()

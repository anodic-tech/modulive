""" . """
from modulive.modulive_surface import ModuliveSurface
from modulive.utils import catch_exception, get_arguments, get_type
from modulive_wootingone.module_key import ModuleKey
from modulive_wootingone.reset_key import ResetKey
from modulive_wootingone.section_key import SectionKey

KEYS = [
    {"name": "2", "note": 4, "functions": ["<SECTION_KEY>(A,0)", "<MODULE_KEY>(A,0)"]},
    {"name": "3", "note": 5, "functions": ["<SECTION_KEY>(A,1)", "<MODULE_KEY>(A,1)"]},
    {"name": "4", "note": 6, "functions": ["<SECTION_KEY>(A,2)", "<MODULE_KEY>(A,2)"]},
    {"name": "5", "note": 7, "functions": ["<SECTION_KEY>(A,3)", "<MODULE_KEY>(A,3)"]},
    {"name": "ctrl", "note": 127, "functions": ["<RESET_KEY>()"]},
]

KEY_TYPES = {"SECTION_KEY": SectionKey, "MODULE_KEY": ModuleKey, "RESET_KEY": ResetKey}


IN_CHANNEL = 0
OUT_CHANNEL = 1


class ModuliveWootingOne(ModuliveSurface):
    """Modulive - WootingOne Integration"""

    @catch_exception
    def __init__(self, *a, **k):
        super().__init__(name="ModuliveWootingOne", *a, **k)
        with self.component_guard():
            self._key_handlers = []
            for key in KEYS:
                for func in key["functions"]:
                    type_name = get_type(func)
                    type_params = get_arguments(func)
                    self._key_handlers.append(
                        KEY_TYPES[type_name](key["name"], key["note"], type_params)
                    )

            self._update_mapping()

    def _update_mapping(self):
        """Get params from Modulive"""
        for handler in self._key_handlers:
            handler.handle_state_change()

    def refresh_state(self):
        """Public accessor for mapping update"""
        self._update_mapping()

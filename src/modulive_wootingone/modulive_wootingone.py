""" . """
from functools import partial
from modulive.modulive_surface import ModuliveSurface
from modulive.utils import catch_exception, get_arguments, get_type
from modulive_wootingone.module_key import (
    handle_module_key_feedback,
    handle_module_key_press,
)
from modulive_wootingone.reset_key import handle_reset_key_press
from modulive_wootingone.section_key import (
    handle_section_key_feedback,
    handle_section_key_press,
)
from modulive_wootingone.wooting_key import WootingKey

KEYS = [
    {"name": "2", "note": 4, "functions": ["<SECTION_KEY>(A,0)", "<MODULE_KEY>(A,0)"]},
    {"name": "3", "note": 5, "functions": ["<SECTION_KEY>(A,1)", "<MODULE_KEY>(A,1)"]},
    {"name": "4", "note": 6, "functions": ["<SECTION_KEY>(A,2)", "<MODULE_KEY>(A,2)"]},
    {"name": "5", "note": 7, "functions": ["<SECTION_KEY>(A,3)", "<MODULE_KEY>(A,3)"]},
    {"name": "ctrl", "note": 127, "functions": ["<RESET_KEY>()"]},
]

KEY_TYPES = {
    "SECTION_KEY": {
        "input": handle_section_key_press,
        "output": handle_section_key_feedback,
    },
    "MODULE_KEY": {
        "input": handle_module_key_press,
        "output": handle_module_key_feedback,
    },
    "RESET_KEY": {"input": handle_reset_key_press},
}


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
                input_handlers = []
                output_handlers = []
                for func in key["functions"]:
                    type_name = get_type(func)
                    type_params = get_arguments(func)

                    if "input" in KEY_TYPES[type_name]:
                        input_handlers.append(
                            partial(
                                KEY_TYPES[type_name]["input"],
                                self.modulive,
                                type_params,
                            )
                        )

                    if "output" in KEY_TYPES[type_name]:
                        output_handlers.append(
                            partial(
                                KEY_TYPES[type_name]["output"],
                                self.modulive,
                                type_params,
                            )
                        )
                self._key_handlers.append(
                    WootingKey(
                        key["name"], key["note"], input_handlers, output_handlers
                    )
                )

            self._update_mapping()

    def _update_mapping(self):
        """Get params from Modulive"""
        for handler in self._key_handlers:
            handler.handle_state_change()

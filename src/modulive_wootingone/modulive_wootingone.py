""" . """
from functools import partial
from modulive.modulive_surface import ModuliveSurface
from modulive.utils import catch_exception, get_arguments, get_type
from modulive_wootingone.modifier_key import (
    handle_modifier_key_feedback,
    handle_modifier_key_press,
)
from modulive_wootingone.module_indicator_key import (
    handle_module_indicator_key_feedback,
    handle_module_indicator_key_press,
)
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
    {"name": "1", "note": 30, "functions": ["<MODULE_INDICATOR_KEY>(A)"]},
    {"name": "2", "note": 31, "functions": ["<SECTION_KEY>(A,0)", "<MODULE_KEY>(A,0)"]},
    {"name": "3", "note": 32, "functions": ["<SECTION_KEY>(A,1)", "<MODULE_KEY>(A,1)"]},
    {"name": "4", "note": 33, "functions": ["<SECTION_KEY>(A,2)", "<MODULE_KEY>(A,2)"]},
    {"name": "5", "note": 34, "functions": ["<SECTION_KEY>(A,3)", "<MODULE_KEY>(A,3)"]},
    {"name": "w", "note": 26, "functions": ["<SECTION_KEY>(A,4)", "<MODULE_KEY>(A,4)"]},
    {"name": "e", "note": 8, "functions": ["<SECTION_KEY>(A,5)", "<MODULE_KEY>(A,5)"]},
    {"name": "r", "note": 21, "functions": ["<SECTION_KEY>(A,6)", "<MODULE_KEY>(A,6)"]},
    {"name": "t", "note": 23, "functions": ["<SECTION_KEY>(A,7)", "<MODULE_KEY>(A,7)"]},
    {"name": "7", "note": 36, "functions": ["<SECTION_KEY>(B,0)", "<MODULE_KEY>(B,0)"]},
    {"name": "8", "note": 37, "functions": ["<SECTION_KEY>(B,1)", "<MODULE_KEY>(B,1)"]},
    {"name": "9", "note": 38, "functions": ["<SECTION_KEY>(B,2)", "<MODULE_KEY>(B,2)"]},
    {"name": "0", "note": 39, "functions": ["<SECTION_KEY>(B,3)", "<MODULE_KEY>(B,3)"]},
    {"name": "u", "note": 24, "functions": ["<SECTION_KEY>(B,4)", "<MODULE_KEY>(B,4)"]},
    {"name": "i", "note": 12, "functions": ["<SECTION_KEY>(B,5)", "<MODULE_KEY>(B,5)"]},
    {"name": "o", "note": 18, "functions": ["<SECTION_KEY>(B,6)", "<MODULE_KEY>(B,6)"]},
    {"name": "p", "note": 19, "functions": ["<SECTION_KEY>(B,7)", "<MODULE_KEY>(B,7)"]},
    {"name": "-", "note": 45, "functions": ["<MODULE_INDICATOR_KEY>(B)"]},
    {"name": "lctrl", "note": 126, "functions": ["<MODIFIER_KEY>(ctrl)"]},
    {"name": "rctrl", "note": 127, "functions": ["<RESET_KEY>()"]},
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
    "MODIFIER_KEY": {
        "input": handle_modifier_key_press,
        "output": handle_modifier_key_feedback,
    },
    "MODULE_INDICATOR_KEY": {
        "input": handle_module_indicator_key_press,
        "output": handle_module_indicator_key_feedback,
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
            self._modifiers = []
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
                                self,
                                self.modulive,
                                type_params,
                            )
                        )

                    if "output" in KEY_TYPES[type_name]:
                        output_handlers.append(
                            partial(
                                KEY_TYPES[type_name]["output"],
                                self,
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

    def get_state(self):
        """Get Wooting internal state"""
        return {"modifiers": self._modifiers}

    def enable_modifier(self, modifier):
        """."""
        if not modifier in self._modifiers:
            self._modifiers.append(modifier)
            # TODO: target modifier keys specifically
            self._update_mapping()

    def disable_modifier(self, modifier):
        """."""
        if modifier in self._modifiers:
            self._modifiers.remove(modifier)
            # TODO: target modifier keys specifically
            self._update_mapping()

    def _update_mapping(self):
        """Get params from Modulive"""
        for handler in self._key_handlers:
            handler.handle_state_change()

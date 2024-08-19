""" . """
from functools import partial
from modulive.modulive_surface import ModuliveSurface
from modulive.utils import catch_exception, get_arguments, get_type
from modulive_wootingone.constants import KEYS
from modulive_wootingone.dynamic_clip_key import (
    handle_dynamic_key_feedback,
    handle_dynamic_key_press,
)
from modulive_wootingone.global_key import (
    handle_global_key_feedback,
    handle_global_key_press,
)
from modulive_wootingone.macro_variation_key import handle_variation_key_feedback, handle_variation_key_press
from modulive_wootingone.wooting_key import WootingKey

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

#TODO: refactor to use extendable classes instead of floating objects
KEY_TYPES = {
    "GLOBAL_KEY": {
        "input": handle_global_key_press,
        "output": handle_global_key_feedback,
    },
    "SECTION_KEY": {
        "input": handle_section_key_press,
        "output": handle_section_key_feedback,
    },
    "DYNAMIC_KEY": {
        "input": handle_dynamic_key_press,
        "output": handle_dynamic_key_feedback,
    },
    "VARIATION_KEY": {
        "input": handle_variation_key_press,
        "output": handle_variation_key_feedback,
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

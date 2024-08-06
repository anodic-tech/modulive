""" . """

KEYS = [
    {"name": "~", "note": 53, "functions": ["<GLOBAL_KEY>()"]},
    {"name": "print", "note": 70, "functions": ["<MODULE_INDICATOR_KEY>(X)"]},
    {"name": "2", "note": 31, "functions": ["<SECTION_KEY>(X,0)", "<MODULE_KEY>(X,0)"]},
    {"name": "3", "note": 32, "functions": ["<SECTION_KEY>(X,1)", "<MODULE_KEY>(X,1)"]},
    {"name": "4", "note": 33, "functions": ["<SECTION_KEY>(X,2)", "<MODULE_KEY>(X,2)"]},
    {"name": "5", "note": 34, "functions": ["<SECTION_KEY>(X,3)", "<MODULE_KEY>(X,3)"]},
    {"name": "w", "note": 26, "functions": ["<SECTION_KEY>(X,4)", "<MODULE_KEY>(X,4)"]},
    {"name": "e", "note": 8, "functions": ["<SECTION_KEY>(X,5)", "<MODULE_KEY>(X,5)"]},
    {"name": "r", "note": 21, "functions": ["<SECTION_KEY>(X,6)", "<MODULE_KEY>(X,6)"]},
    {"name": "t", "note": 23, "functions": ["<SECTION_KEY>(X,7)", "<MODULE_KEY>(X,7)"]},
    {"name": "7", "note": 36, "functions": ["<SECTION_KEY>(Y,0)", "<MODULE_KEY>(Y,0)"]},
    {"name": "8", "note": 37, "functions": ["<SECTION_KEY>(Y,1)", "<MODULE_KEY>(Y,1)"]},
    {"name": "9", "note": 38, "functions": ["<SECTION_KEY>(Y,2)", "<MODULE_KEY>(Y,2)"]},
    {"name": "0", "note": 39, "functions": ["<SECTION_KEY>(Y,3)", "<MODULE_KEY>(Y,3)"]},
    {"name": "u", "note": 24, "functions": ["<SECTION_KEY>(Y,4)", "<MODULE_KEY>(Y,4)"]},
    {"name": "i", "note": 12, "functions": ["<SECTION_KEY>(Y,5)", "<MODULE_KEY>(Y,5)"]},
    {"name": "o", "note": 18, "functions": ["<SECTION_KEY>(Y,6)", "<MODULE_KEY>(Y,6)"]},
    {"name": "p", "note": 19, "functions": ["<SECTION_KEY>(Y,7)", "<MODULE_KEY>(Y,7)"]},
    {"name": "pause", "note": 72, "functions": ["<MODULE_INDICATOR_KEY>(Y)"]},
    {"name": "lshift", "note": 125, "functions": ["<MODIFIER_KEY>(shift)"]},
    {"name": "lctrl", "note": 126, "functions": ["<MODIFIER_KEY>(ctrl)"]},
    {"name": "rctrl", "note": 127, "functions": ["<RESET_KEY>()"]},
]


class Animations:
    """Type mappings to readable variables"""

    DIM = 1
    MEDIUM = 2
    FLASHING = 3

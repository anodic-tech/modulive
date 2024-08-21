""" . """

KEYS = [
    {"name": "escape", "note": 41, "functions": ["<MODIFIER_KEY>(esc)"]},
    {"name": "~", "note": 53, "functions": ["<GLOBAL_KEY>()"]},
    {"name": "print", "note": 70, "functions": ["<MODULE_INDICATOR_KEY>(X)"]},
    {"name": "f1", "note": 58, "functions": ["<VARIATION_KEY>(X,0)"]},
    {"name": "f2", "note": 59, "functions": ["<VARIATION_KEY>(X,1)"]},
    {"name": "f3", "note": 60, "functions": ["<VARIATION_KEY>(X,2)"]},
    {"name": "f4", "note": 61, "functions": ["<VARIATION_KEY>(X,3)"]},
    {"name": "2", "note": 31, "functions": ["<SECTION_KEY>(X,0)", "<MODULE_KEY>(X,0)"]},
    {"name": "3", "note": 32, "functions": ["<SECTION_KEY>(X,1)", "<MODULE_KEY>(X,1)"]},
    {"name": "4", "note": 33, "functions": ["<SECTION_KEY>(X,2)", "<MODULE_KEY>(X,2)"]},
    {"name": "5", "note": 34, "functions": ["<SECTION_KEY>(X,3)", "<MODULE_KEY>(X,3)"]},
    {"name": "w", "note": 26, "functions": ["<SECTION_KEY>(X,4)", "<MODULE_KEY>(X,4)"]},
    {"name": "e", "note": 8, "functions": ["<SECTION_KEY>(X,5)", "<MODULE_KEY>(X,5)"]},
    {"name": "r", "note": 21, "functions": ["<SECTION_KEY>(X,6)", "<MODULE_KEY>(X,6)"]},
    {"name": "t", "note": 23, "functions": ["<SECTION_KEY>(X,7)", "<MODULE_KEY>(X,7)"]},
    {"name": "s", "note": 22, "functions": ["<DYNAMIC_KEY>(X,0)", "<MODULE_KEY>(X,8)"]},
    {"name": "d", "note": 7, "functions": ["<DYNAMIC_KEY>(X,1)", "<MODULE_KEY>(X,9)"]},
    {"name": "f", "note": 9, "functions": ["<DYNAMIC_KEY>(X,2)", "<MODULE_KEY>(X,10)"]},
    {
        "name": "g",
        "note": 10,
        "functions": ["<DYNAMIC_KEY>(X,3)", "<MODULE_KEY>(X,11)"],
    },
    {
        "name": "x",
        "note": 27,
        "functions": ["<DYNAMIC_KEY>(X,4)", "<MODULE_KEY>(X,12)"],
    },
    {"name": "c", "note": 6, "functions": ["<DYNAMIC_KEY>(X,5)", "<MODULE_KEY>(X,13)"]},
    {
        "name": "v",
        "note": 25,
        "functions": ["<DYNAMIC_KEY>(X,6)", "<MODULE_KEY>(X,14)"],
    },
    {"name": "b", "note": 5, "functions": ["<DYNAMIC_KEY>(X,7)", "<MODULE_KEY>(X,15)"]},
    {"name": "f5", "note": 62, "functions": ["<VARIATION_KEY>(Y,0)"]},
    {"name": "f6", "note": 63, "functions": ["<VARIATION_KEY>(Y,1)"]},
    {"name": "f7", "note": 64, "functions": ["<VARIATION_KEY>(Y,2)"]},
    {"name": "f8", "note": 65, "functions": ["<VARIATION_KEY>(Y,3)"]},
    {"name": "7", "note": 36, "functions": ["<SECTION_KEY>(Y,0)", "<MODULE_KEY>(Y,0)"]},
    {"name": "8", "note": 37, "functions": ["<SECTION_KEY>(Y,1)", "<MODULE_KEY>(Y,1)"]},
    {"name": "9", "note": 38, "functions": ["<SECTION_KEY>(Y,2)", "<MODULE_KEY>(Y,2)"]},
    {"name": "0", "note": 39, "functions": ["<SECTION_KEY>(Y,3)", "<MODULE_KEY>(Y,3)"]},
    {"name": "u", "note": 24, "functions": ["<SECTION_KEY>(Y,4)", "<MODULE_KEY>(Y,4)"]},
    {"name": "i", "note": 12, "functions": ["<SECTION_KEY>(Y,5)", "<MODULE_KEY>(Y,5)"]},
    {"name": "o", "note": 18, "functions": ["<SECTION_KEY>(Y,6)", "<MODULE_KEY>(Y,6)"]},
    {"name": "p", "note": 19, "functions": ["<SECTION_KEY>(Y,7)", "<MODULE_KEY>(Y,7)"]},
    {"name": "j", "note": 13, "functions": ["<DYNAMIC_KEY>(Y,0)", "<MODULE_KEY>(Y,8)"]},
    {"name": "k", "note": 14, "functions": ["<DYNAMIC_KEY>(Y,1)", "<MODULE_KEY>(Y,9)"]},
    {
        "name": "l",
        "note": 15,
        "functions": ["<DYNAMIC_KEY>(Y,2)", "<MODULE_KEY>(Y,10)"],
    },
    {
        "name": ";",
        "note": 51,
        "functions": ["<DYNAMIC_KEY>(Y,3)", "<MODULE_KEY>(Y,11)"],
    },
    {
        "name": "m",
        "note": 16,
        "functions": ["<DYNAMIC_KEY>(Y,4)", "<MODULE_KEY>(Y,12)"],
    },
    {
        "name": ",",
        "note": 54,
        "functions": ["<DYNAMIC_KEY>(Y,5)", "<MODULE_KEY>(Y,13)"],
    },
    {
        "name": ".",
        "note": 55,
        "functions": ["<DYNAMIC_KEY>(Y,6)", "<MODULE_KEY>(Y,14)"],
    },
    {
        "name": "/",
        "note": 56,
        "functions": ["<DYNAMIC_KEY>(Y,7)", "<MODULE_KEY>(Y,15)"],
    },
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

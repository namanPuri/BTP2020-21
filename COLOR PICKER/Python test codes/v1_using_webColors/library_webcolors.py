"""
Utility functions for working with the color names and color value
formats defined by the HTML and CSS specifications for use in
documents on the Web.

See documentation (in docs/ directory of source distribution) for
details of the supported formats, conventions and conversions.

"""

import re
import string
from typing import NamedTuple, Tuple, Union


__version__ = "1.11.1"


def _reversedict(d: dict) -> dict:
    """
    Internal helper for generating reverse mappings; given a
    dictionary, returns a new dictionary with keys and values swapped.

    """
    return {value: key for key, value in d.items()}


HEX_COLOR_RE = re.compile(r"^#([a-fA-F0-9]{3}|[a-fA-F0-9]{6})$")

# HTML4 = "html4"
# CSS2 = "css2"
# CSS21 = "css21"
CSS3 = "css3"

#SUPPORTED_SPECIFICATIONS = (HTML4, CSS2, CSS21, CSS3)
SUPPORTED_SPECIFICATIONS = (CSS3)

SPECIFICATION_ERROR_TEMPLATE = "{{spec}} is not a supported specification for color name lookups; \
supported specifications are: {supported}.".format(
    supported=",".join(SUPPORTED_SPECIFICATIONS)
)

IntegerRGB = NamedTuple("IntegerRGB", [("red", int), ("green", int), ("blue", int)])
# PercentRGB = NamedTuple("PercentRGB", [("red", str), ("green", str), ("blue", str)])
# HTML5SimpleColor = NamedTuple(
#     "HTML5SimpleColor", [("red", int), ("green", int), ("blue", int)]
# )

# IntTuple = Union[IntegerRGB, HTML5SimpleColor, Tuple[int, int, int]]
IntTuple = Union[IntegerRGB, Tuple[int, int, int]]
# PercentTuple = Union[PercentRGB, Tuple[str, str, str]]


# Mappings of color names to normalized hexadecimal color values.
#################################################################

# The HTML 4 named colors.
#
# The canonical source for these color definitions is the HTML 4
# specification:
#
# http://www.w3.org/TR/html401/types.html#h-6.5
#
# The file tests/definitions.py in the source distribution of this
# module downloads a copy of the HTML 4 standard and parses out the
# color names to ensure the values below are correct.

# CSS 2 used the same list as HTML 4.
# CSS2_NAMES_TO_HEX = HTML4_NAMES_TO_HEX

# CSS 2.1 added orange.
# CSS21_NAMES_TO_HEX = {"orange": "#ffa500", **HTML4_NAMES_TO_HEX}

# The CSS 3/SVG named colors.
#
# The canonical source for these color definitions is the SVG
# specification's color list (which was adopted as CSS 3's color
# definition):
#
# http://www.w3.org/TR/SVG11/types.html#ColorKeywords
#
# CSS 3 also provides definitions of these colors:
#
# http://www.w3.org/TR/css3-color/#svg-color
#
# SVG provides the definitions as RGB triplets. CSS 3 provides them
# both as RGB triplets and as hexadecimal. Since hex values are more
# common in real-world HTML and CSS, the mapping below is to hex
# values instead. The file tests/definitions.py in the source
# distribution of this module downloads a copy of the CSS 3 color
# module and parses out the color names to ensure the values below are
# correct.
CSS3_NAMES_TO_HEX = {
    # "aliceblue": "#f0f8ff",
    # "antiquewhite": "#faebd7",
    # "aqua": "#00ffff",
    # "aquamarine": "#7fffd4",
    # "azure": "#f0ffff",
    # "beige": "#f5f5dc",
    # "bisque": "#ffe4c4",
    "black": "#000000",
    # "blanchedalmond": "#ffebcd",
    "blue": "#0000ff",
    # "blueviolet": "#8a2be2",
    "brown": "#a52a2a",
    # "burlywood": "#deb887",
    # "cadetblue": "#5f9ea0",
    # "chartreuse": "#7fff00",
    # "chocolate": "#d2691e",
    # "coral": "#ff7f50",
    # "cornflowerblue": "#6495ed",
    # "cornsilk": "#fff8dc",
    # "crimson": "#dc143c",
    # "cyan": "#00ffff",
    "darkblue": "#00008b",
    # "darkcyan": "#008b8b",
    # "darkgoldenrod": "#b8860b",
    "darkgray": "#a9a9a9",
    # "darkgrey": "#a9a9a9",
    "darkgreen": "#006400",
    # "darkkhaki": "#bdb76b",
    # "darkmagenta": "#8b008b",
    # "darkolivegreen": "#556b2f",
    "darkorange": "#ff8c00",
    # "darkorchid": "#9932cc",
    "darkred": "#8b0000",
    # "darksalmon": "#e9967a",
    # "darkseagreen": "#8fbc8f",
    # "darkslateblue": "#483d8b",
    # "darkslategray": "#2f4f4f",
    # "darkslategrey": "#2f4f4f",
    # "darkturquoise": "#00ced1",
    # "darkviolet": "#9400d3",
    # "deeppink": "#ff1493",
    # "deepskyblue": "#00bfff",
    # "dimgray": "#696969",
    # "dimgrey": "#696969",
    # "dodgerblue": "#1e90ff",
    # "firebrick": "#b22222",
    # "floralwhite": "#fffaf0",
    # "forestgreen": "#228b22",
    # "fuchsia": "#ff00ff",
    # "gainsboro": "#dcdcdc",
    # "ghostwhite": "#f8f8ff",
    # "gold": "#ffd700",
    # "goldenrod": "#daa520",
    "gray": "#808080",
    # "grey": "#808080",
    "green": "#008000",
    # "greenyellow": "#adff2f",
    # "honeydew": "#f0fff0",
    # "hotpink": "#ff69b4",
    # "indianred": "#cd5c5c",
    # "indigo": "#4b0082",
    # "ivory": "#fffff0",
    # "khaki": "#f0e68c",
    # "lavender": "#e6e6fa",
    # "lavenderblush": "#fff0f5",
    # "lawngreen": "#7cfc00",
    # "lemonchiffon": "#fffacd",
    "lightblue": "#add8e6",
    # "lightcoral": "#f08080",
    # "lightcyan": "#e0ffff",
    # "lightgoldenrodyellow": "#fafad2",
    # "lightgray": "#d3d3d3",
    # "lightgrey": "#d3d3d3",
    "lightgreen": "#90ee90",
    "lightpink": "#ffb6c1",
    # "lightsalmon": "#ffa07a",
    # "lightseagreen": "#20b2aa",
    # "lightskyblue": "#87cefa",
    # "lightslategray": "#778899",
    # "lightslategrey": "#778899",
    # "lightsteelblue": "#b0c4de",
    "lightyellow": "#ffffe0",
    # "lime": "#00ff00",
    # "limegreen": "#32cd32",
    # "linen": "#faf0e6",
    # "magenta": "#ff00ff",
    # "maroon": "#800000",
    # "mediumaquamarine": "#66cdaa",
    "mediumblue": "#0000cd",
    # "mediumorchid": "#ba55d3",
    # "mediumpurple": "#9370db",
    # "mediumseagreen": "#3cb371",
    # "mediumslateblue": "#7b68ee",
    # "mediumspringgreen": "#00fa9a",
    # "mediumturquoise": "#48d1cc",
    # "mediumvioletred": "#c71585",
    # "midnightblue": "#191970",
    # "mintcream": "#f5fffa",
    # "mistyrose": "#ffe4e1",
    # "moccasin": "#ffe4b5",
    # "navajowhite": "#ffdead",
    # "navy": "#000080",
    # "oldlace": "#fdf5e6",
    # "olive": "#808000",
    # "olivedrab": "#6b8e23",
    "orange": "#ffa500",
    # "orangered": "#ff4500",
    # "orchid": "#da70d6",
    # "palegoldenrod": "#eee8aa",
    # "palegreen": "#98fb98",
    # "paleturquoise": "#afeeee",
    # "palevioletred": "#db7093",
    # "papayawhip": "#ffefd5",
    # "peachpuff": "#ffdab9",
    # "peru": "#cd853f",
    "pink": "#ffc0cb",
    # "plum": "#dda0dd",
    # "powderblue": "#b0e0e6",
    # "purple": "#800080",
    "red": "#ff0000",
    # "rosybrown": "#bc8f8f",
    # "royalblue": "#4169e1",
    # "saddlebrown": "#8b4513",
    # "salmon": "#fa8072",
    # "sandybrown": "#f4a460",
    "seagreen": "#2e8b57",
    # "seashell": "#fff5ee",
    # "sienna": "#a0522d",
    "silver": "#c0c0c0",
    "skyblue": "#87ceeb",
    # "slateblue": "#6a5acd",
    # "slategray": "#708090",
    # "slategrey": "#708090",
    # "snow": "#fffafa",
    # "springgreen": "#00ff7f",
    # "steelblue": "#4682b4",
    # "tan": "#d2b48c",
    # "teal": "#008080",
    # "thistle": "#d8bfd8",
    # "tomato": "#ff6347",
    # "turquoise": "#40e0d0",
    # "violet": "#ee82ee",
    # "wheat": "#f5deb3",
    "white": "#ffffff",
    # "whitesmoke": "#f5f5f5",
    "yellow": "#ffff00",
    # "yellowgreen": "#9acd32",
}


# Mappings of normalized hexadecimal color values to color names.
#################################################################

CSS3_HEX_TO_NAMES = _reversedict(CSS3_NAMES_TO_HEX)

# Normalization functions.
#################################################################


def normalize_hex(hex_value: str) -> str:
    """
    Normalize a hexadecimal color value to 6 digits, lowercase.

    """
    match = HEX_COLOR_RE.match(hex_value)
    if match is None:
        raise ValueError(
            "'{}' is not a valid hexadecimal color value.".format(hex_value)
        )
    hex_digits = match.group(1)
    if len(hex_digits) == 3:
        hex_digits = "".join(2 * s for s in hex_digits)
    return "#{}".format(hex_digits.lower())


def _normalize_integer_rgb(value: int) -> int:
    """
    Internal normalization function for clipping integer values into
    the permitted range (0-255, inclusive).

    """
    return 0 if value < 0 else 255 if value > 255 else value


def normalize_integer_triplet(rgb_triplet: IntTuple) -> IntegerRGB:
   """
   Normalize an integer ``rgb()`` triplet so that all values are
   within the range 0-255 inclusive.

   """
   return IntegerRGB._make(_normalize_integer_rgb(value) for value in rgb_triplet)

# Conversions from hexadecimal color values to various formats.
#################################################################


def hex_to_name(hex_value: str, spec: str = CSS3) -> str:
   """
   Convert a hexadecimal color value to its corresponding normalized
   color name, if any such name exists.

   The optional keyword argument ``spec`` determines which
   specification's list of color names will be used. The default is
   CSS3.

   When no color name for the value is found in the given
   specification, ``ValueError`` is raised.

   """
   if spec not in SUPPORTED_SPECIFICATIONS:
       raise ValueError(SPECIFICATION_ERROR_TEMPLATE.format(spec=spec))
   normalized = normalize_hex(hex_value)
   name = {
       # CSS2: CSS2_HEX_TO_NAMES,
       # CSS21: CSS21_HEX_TO_NAMES,
       CSS3: CSS3_HEX_TO_NAMES,
       # HTML4: HTML4_HEX_TO_NAMES,
   }[spec].get(normalized)
   if name is None:
       raise ValueError("'{}' has no defined color name in {}".format(hex_value, spec))
   return name


def hex_to_rgb(hex_value: str) -> IntegerRGB:
   """
   Convert a hexadecimal color value to a 3-tuple of integers
   suitable for use in an ``rgb()`` triplet specifying that color.

   """
   int_value = int(normalize_hex(hex_value)[1:], 16)
   return IntegerRGB(int_value >> 16, int_value >> 8 & 0xFF, int_value & 0xFF)

# Conversions from  integer rgb() triplets to various formats.
#################################################################


def rgb_to_name(rgb_triplet: IntTuple, spec: str = CSS3) -> str:
    """
    Convert a 3-tuple of integers, suitable for use in an ``rgb()``
    color triplet, to its corresponding normalized color name, if any
    such name exists.

    The optional keyword argument ``spec`` determines which
    specification's list of color names will be used. The default is
    CSS3.

    If there is no matching name, ``ValueError`` is raised.

    """
    return hex_to_name(rgb_to_hex(normalize_integer_triplet(rgb_triplet)), spec=spec)


def rgb_to_hex(rgb_triplet: IntTuple) -> str:
   """
   Convert a 3-tuple of integers, suitable for use in an ``rgb()``
   color triplet, to a normalized hexadecimal value for that color.

   """
   return "#{:02x}{:02x}{:02x}".format(*normalize_integer_triplet(rgb_triplet))

# def _percent_to_integer(percent: str) -> int:
#     """
#     Internal helper for converting a percentage value to an integer
#     between 0 and 255 inclusive.

#     """
#     return int(round(float(percent.split("%")[0]) / 100 * 255))

def html5_serialize_simple_color(simple_color: IntTuple) -> str:
    """
    Apply the serialization algorithm for a simple color from section
    2.4.6 of HTML5.

    """
    red, green, blue = simple_color

    # 1. Let result be a string consisting of a single "#" (U+0023)
    #    character.
    result = "#"

    # 2. Convert the red, green, and blue components in turn to
    #    two-digit hexadecimal numbers using lowercase ASCII hex
    #    digits, zero-padding if necessary, and append these numbers
    #    to result, in the order red, green, blue.
    format_string = "{:02x}"
    result += format_string.format(red)
    result += format_string.format(green)
    result += format_string.format(blue)

    # 3. Return result, which will be a valid lowercase simple color.
    return result

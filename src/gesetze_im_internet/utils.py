# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

import re

from lxml import etree

from gesetze_im_internet.GesetzNode import GesetzNode


NODE_WRAPPER_CLASSES: dict[str, GesetzNode] = {}


def register(cls: GesetzNode):
    NODE_WRAPPER_CLASSES[cls.TAG] = cls
    return cls


def wrap_node(node: etree._Element):
    return NODE_WRAPPER_CLASSES[node.tag](node=node)


def int2roman(number: int) -> str:
    """Converts an int to its roman value.

    References:
        https://www.geeksforgeeks.org/python/python-program-to-convert-integer-to-roman/
    """
    int2roman_map = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]

    roman = ""
    while number > 0:
        for int_base, roman_base in int2roman_map:
            while number >= int_base:
                roman += roman_base
                number -= int_base
    return roman


def alphanumeric2float(alphanumeric: str) -> float:
    """Convert a alphanumeric ordering number to a float."""
    match = re.search(r"\d([a-z])$", alphanumeric)
    if match:
        return (
            float(alphanumeric.removesuffix(match.group(1)))
            + (ord(match.group(1)) - 96) / 100
        )
    return float(alphanumeric)


def float2alphanumeric(float_input: float) -> str:
    """Convert a float to a alphanumeric ordering number."""
    remainder = float_input % 1
    if remainder:
        return str(int(float_input - remainder)) + chr(int(remainder * 100) + 96)
    return str(int(float_input))


def replace_umlauts(string: str) -> str:
    return re.sub(r"[äüöß]", "_", string)

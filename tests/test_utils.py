# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

import pytest

from gesetze_im_internet import utils


@pytest.mark.parametrize(
    "alphanumeric,expected_float",
    [
        ("23a", 23.01),
        ("1", 1),
    ],
)
def test_alphanumeric2float(alphanumeric, expected_float):
    assert utils.alphanumeric2float(alphanumeric) == expected_float


@pytest.mark.parametrize(
    "float_input,expected_alphanumeric",
    [
        (23.01, "23a"),
        (1, "1"),
    ],
)
def test_float2alphanumeric(float_input, expected_alphanumeric):
    assert utils.float2alphanumeric(float_input) == expected_alphanumeric


@pytest.mark.parametrize(
    "umlautsstr,expected_str",
    [
        ("ätest", "_test"),
        ("abcßdef", "abc_def"),
        ("asdf", "asdf"),
    ],
)
def test_replace_umlauts(umlautsstr, expected_str):
    assert utils.replace_umlauts(umlautsstr) == expected_str


@pytest.mark.parametrize(
    "integer,expected_roman",
    [
        (1, "I"),
        (12, "XII"),
        (36, "XXXVI"),
    ],
)
def test_int2roman(integer, expected_roman):
    assert utils.int2roman(integer) == expected_roman

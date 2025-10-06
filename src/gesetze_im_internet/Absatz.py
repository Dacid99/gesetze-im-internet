# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

from __future__ import annotations

import re
from typing import TYPE_CHECKING

from gesetze_im_internet.exceptions import ImproperTagError
from gesetze_im_internet.utils import int2roman, register, wrap_node


if TYPE_CHECKING:
    from collections.abc import Iterable

    from lxml import etree

    from .Norm import Norm


@register
class Absatz:
    TAG = "P"
    NR_REGEX = r"^\s*\(\s*(\d+)\s*\)"
    STR_TEMPLATE = "%(norm)s %(nr)s"

    def __init__(self, absatz_node: etree.Element) -> None:
        if absatz_node.tag != self.TAG:
            raise ImproperTagError()
        self._absatz_node = absatz_node

    def __int__(self) -> int:
        return self.nr or 1

    def __str__(self) -> str:
        return self._absatz_node.text or ""

    def __repr__(self) -> str:
        return self.STR_TEMPLATE % {
            "norm": repr(self.norm),
            "nr": (int2roman(self.nr) if self.nr else "I"),
        }

    def __iter__(self) -> Iterable[str]:
        for sentence in self._absatz_node.text.split(". "):
            yield sentence.strip()

    @property
    def nr(self) -> int | None:
        text = self._absatz_node.text
        if text:
            nr_match = re.search(self.NR_REGEX, text)
            if nr_match:
                return int(nr_match.group(1))
        return None

    @property
    def norm(self) -> Norm:
        norm_candidate = self._absatz_node.getparent()
        while norm_candidate.tag != "norm":
            norm_candidate = norm_candidate.getparent()
        return wrap_node(norm_candidate)

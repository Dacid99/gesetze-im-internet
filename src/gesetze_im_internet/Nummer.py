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

from typing import TYPE_CHECKING

from gesetze_im_internet.exceptions import ImproperTagError
from gesetze_im_internet.utils import register, wrap_node


if TYPE_CHECKING:
    from lxml import etree

    from .Satz import Satz


@register
class Nummer:
    TAG = "DT"
    STR_TEMPLATE = "%(satz)s Nr. %(nr)s"

    def __init__(self, node: etree._Element) -> None:
        if node.tag != self.TAG:
            raise ImproperTagError
        self._nummer_node = node

    def __int__(self) -> int:
        return self.nr or 1

    def __str__(self) -> str:
        return self._nummer_node.findtext(".//LA") or ""

    def __repr__(self) -> str:
        return self.STR_TEMPLATE % {"satz": repr(self.satz), "nr": int(self)}

    @property
    def nr(self) -> int | None:
        try:
            nr = (
                int(self._nummer_node.text.strip(". "))
                if self._nummer_node.text
                else None
            )
        except ValueError:
            nr = None
        return nr

    @property
    def satz(self) -> Satz:
        satz_candidate = self._nummer_node.getparent()
        while satz_candidate.tag != "satz":
            satz_candidate = satz_candidate.getparent()
        return wrap_node(satz_candidate)

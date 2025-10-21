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
    from collections.abc import Iterator

    from lxml import etree

    from .Absatz import Absatz
    from .Nummer import Nummer


@register
class Satz:
    TAG = "satz"
    STR_TEMPLATE = "%(absatz)s S. %(nr)s"

    def __init__(self, node: etree._Element) -> None:
        if node.tag != self.TAG:
            raise ImproperTagError("")
        self._satz_node = node

    def __int__(self) -> int:
        return self.nr or 1

    def __iter__(self) -> Iterator[Nummer]:
        for nummer_dt, nummer_dd in zip(
            self._satz_node.findall(".//DT"), self._satz_node.findall(".//DD")
        ):
            nummer_dt.append(nummer_dd)
            yield wrap_node(nummer_dt)

    def __len__(self) -> int:
        return len(self._satz_node.findall(".//DT"))

    def __str__(self) -> str:
        return self._satz_node.text + "".join([str(nummer) for nummer in self])

    def __repr__(self) -> str:
        return self.STR_TEMPLATE % {"absatz": repr(self.absatz), "nr": int(self)}

    def __getitem__(self, index: int) -> Nummer:
        return wrap_node(self._satz_node.findall(".//DT")[index])

    def __call__(self, index: int) -> Nummer:
        return self[index]

    @property
    def nr(self) -> int | None:
        return int(self._satz_node["nr"])

    @property
    def absatz(self) -> Absatz:
        """The absatz that this satz is a part of."""
        norm_candidate = self._satz_node.getparent()
        while norm_candidate is not None and norm_candidate.tag != "satz":
            norm_candidate = norm_candidate.getparent()
        return wrap_node(norm_candidate) if norm_candidate is not None else None

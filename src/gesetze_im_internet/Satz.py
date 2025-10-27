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

from typing_extensions import override

from gesetze_im_internet.GesetzNode import GesetzNode
from gesetze_im_internet.utils import _register, _wrap_node


if TYPE_CHECKING:
    from collections.abc import Iterator

    from lxml import etree

    from .Absatz import Absatz
    from .Nummer import Nummer


@_register
class Satz(GesetzNode):
    """Wrapper class for the satz gii-xml element."""

    TAG = "satz"
    STR_TEMPLATE = "%(absatz)s S. %(nr)s"

    def __init__(self, node: etree._Element) -> None:
        super().__init__(node)

    def __int__(self) -> int:
        """The number of this Satz."""
        return self.nr or 1

    def __iter__(self) -> Iterator[Nummer]:
        """Iterator over the Nummern in this Satz."""
        for nummer_dt in self._node.findall(".//DT"):
            yield _wrap_node(nummer_dt)

    def __len__(self) -> int:
        """The number of Nummern in this Satz."""
        return len(self._node.findall(".//DT"))

    @override
    def __str__(self) -> str:
        """The text content of this Satz."""
        string = (self._node.text or "") + "".join(
            [
                str(int(nummer)) + ". " + str(nummer) + (nummer._node.tail or " ")
                for nummer in self
            ]
        )
        return string + ". " if not string.endswith((". ", ".")) else string

    @override
    def __repr__(self) -> str:
        """The full reference to this Satz."""
        return self.STR_TEMPLATE % {"absatz": repr(self.absatz), "nr": int(self)}

    def __getitem__(self, index: int | slice) -> Nummer | list[Nummer]:
        """Gets a Nummer by index."""
        nodes = self._node.findall(".//DT")[index]
        if isinstance(nodes, list):
            return [_wrap_node(node) for node in nodes]
        return _wrap_node(nodes)

    def __call__(self, nummer_nr: int) -> Nummer | None:
        """Gets a Nummer by its number."""
        for nummer in self:
            if int(nummer) == nummer_nr:
                return nummer
        return None

    @property
    def nr(self) -> int | None:
        """The number of this Satz."""
        return int(self._node.attrib["nr"])

    @property
    def absatz(self) -> Absatz:
        """The absatz that this satz is a part of."""
        norm_candidate = self._node.getparent()
        while norm_candidate is not None and norm_candidate.tag != "P":
            norm_candidate = norm_candidate.getparent()
        return _wrap_node(norm_candidate) if norm_candidate is not None else None

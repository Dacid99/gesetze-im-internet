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

from lxml import etree
from typing_extensions import override

from gesetze_im_internet.exceptions import ImproperTagError
from gesetze_im_internet.GesetzNode import GesetzNode
from gesetze_im_internet.utils import int2roman, register, wrap_node


if TYPE_CHECKING:
    from collections.abc import Iterable

    from .Norm import Norm
    from .Satz import Satz


@register
class Absatz(GesetzNode):
    """A wrapper for a P xml element."""

    TAG = "P"
    NR_REGEX = r"^\s*\(\s*(\d+)\s*\)"
    STR_TEMPLATE = "%(norm)s %(nr)s"

    @override
    def __init__(self, node: etree._Element) -> None:
        if node.tag != self.TAG:
            raise ImproperTagError("")
        self._node = node
        self._modify_node()

    def __int__(self) -> int:
        """The ordering number for this absatz. 1 if no number is given in the text."""
        return self.nr or 1

    @override
    def __str__(self) -> str:
        """The text for this absatz."""
        return "".join([str(satz) for satz in self])

    @override
    def __repr__(self) -> str:
        """The complete reference to this absatz."""
        return self.STR_TEMPLATE % {
            "norm": repr(self.norm),
            "nr": (int2roman(int(self))),
        }

    def __len__(self) -> int:
        """The number of sentences in this absatz."""
        return len(self._node.findall(".//satz"))

    def __iter__(self) -> Iterable[str]:
        """Iterator over all sentences in the absatz."""
        for satz in self._node.iterfind(".//satz"):
            yield wrap_node(satz)

    def __getitem__(self, index: int) -> Satz:
        return wrap_node(self._node.findall(".//satz")[index])

    def __call__(self, index: int) -> Satz:
        return self[index]

    @property
    def nr(self) -> int | None:
        """The ordering number for this absatz. None if no number is given in the text."""
        text = self._node.text
        if text:
            nr_match = re.search(self.NR_REGEX, text)
            if nr_match:
                return int(nr_match.group(1))
        return None

    @property
    def norm(self) -> Norm | None:
        """The norm that this absatz is a part of."""
        norm_candidate = self._node.getparent()
        while norm_candidate is not None and norm_candidate.tag != "norm":
            norm_candidate = norm_candidate.getparent()
        return wrap_node(norm_candidate) if norm_candidate is not None else None

    def _modify_node(self):
        for nummer in self._node.findall(".//DL"):
            nummer_contents = nummer.findall(".//LA")
            if nummer_contents and nummer_contents[-1].text.strip().endswith("."):
                nummer.tail = nummer.tail + ". " if nummer.tail else ". "
        absatz_text = (
            etree.tostring(self._node).removeprefix(b"<P>").removesuffix(b"</P>")
        )
        absatz_text = re.sub(rb"<DL.*</DL>", b"<nummern/>", absatz_text)
        for satz_nr, satz in enumerate(absatz_text.split(b". ")):
            satz_node = etree.SubElement(self._node, "satz", {"nr": str(satz_nr + 1)})
            satz_parts = satz.split(b"<nummern/>")
            if len(satz_parts) > 1:
                satz_node.text = satz_parts[0]
                satz_node.append(self._node.find(".//DL"))
                satz_node.find("DL").tail = satz_parts[1]
            else:
                satz_node.text = satz_parts[0] + b"."

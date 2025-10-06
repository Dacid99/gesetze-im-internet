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
from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING

from gesetze_im_internet.constants import BUILDDATE_FORMAT, TIMEZONE, WEB_PROTOCOL
from gesetze_im_internet.exceptions import ImproperTagError
from gesetze_im_internet.utils import register, replace_umlauts, wrap_node


if TYPE_CHECKING:
    from collections.abc import Iterable

    from lxml import etree

    from .Absatz import Absatz
    from .Dokument import Dokument


@register
class Norm:
    TAG = "norm"
    STR_NORM_TEMPLATE = "%(jurabk)s %(enbez)s %(titel)s"
    STR_GLIEDERUNG_TEMPLATE = "%(jurabk)s %(gliederungsbez)s %(gliederungstitel)s"
    URL_NORM_TEMPLATE = (
        WEB_PROTOCOL + "www.gesetze-im-internet.de/%(jurabk)s/__%(nr)s.html"
    )
    URL_GLIEDERUNG_TEMPLATE = (
        WEB_PROTOCOL
        + "www.gesetze-im-internet.de/%(jurabk)s/%(dokument_doknr)s.html#%(doknr)s"
    )

    def __init__(self, norm_node: etree.Element) -> None:
        if norm_node.tag != self.TAG:
            raise ImproperTagError()
        self._norm_node = norm_node

    def __iter__(self) -> Iterable[Absatz]:
        for absatz_node in self._norm_node.iterfind(".//P"):
            yield wrap_node(absatz_node)

    def __call__(self, absatz_nr: int) -> Absatz:
        return self[absatz_nr]

    def __getitem__(self, absatz_nr: int) -> Absatz:
        return wrap_node(self._norm_node.findall(".//P")[absatz_nr])

    def __str__(self) -> str:
        return "\n".join([f"({int(absatz)}) {absatz}" for absatz in self])

    def __repr__(self) -> str:
        return (
            self.STR_GLIEDERUNG_TEMPLATE
            % {
                "jurabk": self.jurabk,
                "gliederungsbez": self.gliederungsbez,
                "gliederungstitel": self.gliederungstitel,
            }
            if self.is_gliederung
            else self.STR_NORM_TEMPLATE
            % {"jurabk": self.jurabk, "enbez": self.enbez, "titel": self.titel}
        )

    def __int__(self) -> int:
        return (
            int(self.gliederungskennzahl or 0) if self.is_gliederung else (self.nr or 0)
        )

    def __len__(self) -> int:
        return len(self._norm_node.findall(".//P"))

    @property
    def is_gliederung(self) -> bool:
        return self._gliederungseinheit is not None

    @property
    def href(self) -> str:
        return (
            self.URL_GLIEDERUNG_TEMPLATE
            % {
                "jurabk": replace_umlauts(self.jurabk.lower()),
                "dokument_doknr": self.dokument.doknr,
                "doknr": self.doknr,
            }
            if self.is_gliederung
            else self.URL_NORM_TEMPLATE
            % {"jurabk": replace_umlauts(self.jurabk.lower()), "nr": self.nr}
        )

    @cached_property
    def _metadaten(self):
        return self._norm_node.find("metadaten")

    @cached_property
    def _textdaten(self):
        return self._norm_node.find("textdaten")

    @property
    def builddate(self) -> datetime | None:
        builddate = self._norm_node.attrib.get("builddate")
        return (
            datetime.strptime(builddate, BUILDDATE_FORMAT).astimezone(TIMEZONE)
            if builddate
            else None
        )

    @property
    def doknr(self) -> str | None:
        return self._norm_node.attrib.get("doknr")

    @property
    def jurabk(self) -> str | None:
        return self._metadaten.findtext("jurabk")

    @property
    def amtabk(self) -> str | None:
        return self._metadaten.findtext("amtabk")

    @property
    def enbez(self) -> str | None:
        return self._metadaten.findtext("enbez")

    @property
    def titel(self) -> str | None:
        return self._metadaten.findtext("titel")

    @property
    def titel_format(self) -> str | None:
        return self._metadaten.find("titel").attrib.get("format")

    @property
    def nr(self) -> int | None:
        if self.enbez:
            nr_match = re.search(r"(\d+)", self.enbez)
            if nr_match:
                return int(nr_match.group(1))
        return None

    @cached_property
    def _gliederungseinheit(self):
        return self._metadaten.find("gliederungseinheit")

    @property
    def gliederungskennzahl(self) -> str | None:
        return self._gliederungseinheit.findtext("gliederungskennzahl")

    @property
    def gliederungsbez(self) -> str | None:
        return self._gliederungseinheit.findtext("gliederungsbez")

    @property
    def gliederungstitel(self) -> str | None:
        return self._gliederungseinheit.findtext("gliederungstitel")

    @property
    def dokument(self) -> Dokument:
        dokument_candidate = self._norm_node.getparent()
        while dokument_candidate.tag != "dokumente":
            dokument_candidate = dokument_candidate.getparent()
        return wrap_node(dokument_candidate)

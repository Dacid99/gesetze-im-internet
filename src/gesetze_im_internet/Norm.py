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

from datetime import datetime
from functools import cached_property
from typing import TYPE_CHECKING

from typing_extensions import override

from gesetze_im_internet.constants import BUILDDATE_FORMAT, TIMEZONE, WEB_PROTOCOL
from gesetze_im_internet.GesetzNode import GesetzNode
from gesetze_im_internet.utils import (
    alphanumeric2float,
    register,
    replace_umlauts,
    wrap_node,
)


if TYPE_CHECKING:
    from collections.abc import Iterable

    from lxml import etree

    from .Absatz import Absatz
    from .Dokument import Dokument


@register
class Norm(GesetzNode):
    """Wrapper class for the norm gii-xml element."""

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

    def __iter__(self) -> Iterable[Absatz]:
        """Iterator over the absätze in the norm."""
        for absatz_node in self._node.iterfind(".//P"):
            yield wrap_node(absatz_node)

    def __call__(self, absatz_nr: int) -> Absatz | None:
        """Gets an absatz by its number."""
        for absatz in self:
            if int(absatz) == absatz_nr:
                return absatz
        return None

    def __getitem__(self, absatz_nr: int) -> Absatz:
        """Gets an absatz by index."""
        nodes = self._node.findall(".//P")[absatz_nr]
        if isinstance(nodes, list):
            return [wrap_node(node) for node in nodes]
        return wrap_node(nodes)

    @override
    def __str__(self) -> str:
        """The text content of this norm."""
        return "\n".join([str(absatz) for absatz in self])

    @override
    def __repr__(self) -> str:
        """The full reference to this norm."""
        return (
            self.STR_GLIEDERUNG_TEMPLATE
            % {
                "jurabk": self.jurabk or "",
                "gliederungsbez": self.gliederungsbez or "",
                "gliederungstitel": self.gliederungstitel or "",
            }
            if self.is_gliederung
            else self.STR_NORM_TEMPLATE
            % {
                "jurabk": self.jurabk or "",
                "enbez": self.enbez or "",
                "titel": self.titel or "",
            }
        )

    def __int__(self) -> int:
        """The number (paragraph or gliederung) of this norm."""
        return int(float(self))

    def __float__(self) -> float:
        """The number (paragraph or gliederung) of this norm."""
        return (
            (float(self.gliederungskennzahl or 0))
            if self.is_gliederung
            else (self.nr or 0.0)
        )

    def __len__(self) -> int:
        """The number of absätze in this norm."""
        return len(self._node.findall(".//P"))

    @property
    def is_gliederung(self) -> bool:
        """Whether this norm is a law or structuring element."""
        return self._gliederungseinheit is not None

    @property
    def href(self) -> str:
        """The url under which the html version of this law can be found."""
        return (
            self.URL_GLIEDERUNG_TEMPLATE
            % {
                "jurabk": replace_umlauts(self.jurabk.lower()) if self.jurabk else "",
                "dokument_doknr": self.dokument.doknr,
                "doknr": self.doknr,
            }
            if self.is_gliederung
            else self.URL_NORM_TEMPLATE
            % {
                "jurabk": replace_umlauts(self.jurabk.lower()) if self.jurabk else "",
                "nr": self.nr,
            }
        )

    @cached_property
    def _metadaten(self) -> etree._Element | None:
        return self._node.find("metadaten")

    @cached_property
    def _textdaten(self) -> etree._Element | None:
        return self._node.find("textdaten")

    @property
    def builddate(self) -> datetime | None:
        """The datetime the underlying xml was built."""
        builddate = self._node.get("builddate")
        return (
            datetime.strptime(builddate, BUILDDATE_FORMAT).astimezone(TIMEZONE)
            if builddate
            else None
        )

    @property
    def doknr(self) -> str | None:
        """The document number of the underlying xml file."""
        return self._node.get("doknr")

    @property
    def jurabk(self) -> str | None:
        """The common abbreviation of the document name ('Juristische Abkürzung')."""
        return (
            self._metadaten.findtext("jurabk") if self._metadaten is not None else None
        )

    @property
    def amtabk(self) -> str | None:
        """The official abbreviation of the document name ('Amtliche Abkürzung')."""
        return (
            self._metadaten.findtext("amtabk") if self._metadaten is not None else None
        )

    @property
    def enbez(self) -> str | None:
        """The short reference for this law (paragraph notation)."""
        return (
            self._metadaten.findtext("enbez") if self._metadaten is not None else None
        )

    @property
    def titel(self) -> str | None:
        """The title of this law."""
        return (
            self._metadaten.findtext("titel") if self._metadaten is not None else None
        )

    @property
    def titel_format(self) -> str | None:
        """The format of this laws title."""
        if self._metadaten is not None:
            titel = self._metadaten.find("titel")
            if titel is not None:
                return titel.get("format")
        return None

    @property
    def nr(self) -> float | None:
        """The paragraph number of this law."""
        if self.enbez:
            return alphanumeric2float(self.enbez.strip(" §"))
        return None

    @cached_property
    def _gliederungseinheit(self) -> etree._Element | None:
        return (
            self._metadaten.find("gliederungseinheit")
            if self._metadaten is not None
            else None
        )

    @property
    def gliederungskennzahl(self) -> str | None:
        """The Kennzahl of this Gliederungseinheit."""
        return (
            self._gliederungseinheit.findtext("gliederungskennzahl")
            if self.is_gliederung is not None
            else None
        )

    @property
    def gliederungsbez(self) -> str | None:
        """The Bezeichnung of this Gliederungseinheit."""
        return (
            self._gliederungseinheit.findtext("gliederungsbez")
            if self.is_gliederung is not None
            else None
        )

    @property
    def gliederungstitel(self) -> str | None:
        """The Titel of this Gliederungseinheit."""
        return (
            self._gliederungseinheit.findtext("gliederungstitel")
            if self.is_gliederung is not None
            else None
        )

    @property
    def dokument(self) -> Dokument | None:
        """The Dokument that this Norm is a part of."""
        dokument_candidate = self._node
        while dokument_candidate is not None and dokument_candidate.tag != "dokumente":
            dokument_candidate = dokument_candidate.getparent()
        return wrap_node(dokument_candidate) if dokument_candidate is not None else None

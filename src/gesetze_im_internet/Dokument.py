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
from io import BytesIO
from typing import TYPE_CHECKING
from zipfile import ZipFile

from lxml import etree
from requests import get
from typing_extensions import overload, override

from gesetze_im_internet.constants import BUILDDATE_FORMAT, TIMEZONE, WEB_PROTOCOL
from gesetze_im_internet.exceptions import BadDataError, ValidationError
from gesetze_im_internet.utils import register, replace_umlauts, wrap_node


if TYPE_CHECKING:
    from collections.abc import Iterable

    from .Norm import Norm


@register
class Dokument:
    """A wrapper for a dokumente xml element."""

    TAG = "dokumente"
    URL_TEMPLATE = WEB_PROTOCOL + "www.gesetze-im-internet.de/%(jurabk)s/index.html"

    @override
    def __init__(
        self,
        node: etree._Element | None = None,
        book_url: str | None = None,
        validate: bool = False,
    ) -> None:
        if book_url:
            self.parse(self.get(book_url))
            if validate:
                self.validate()
        elif node is not None:
            self._dokumente = node
            if validate:
                self.validate()

    def __iter__(self) -> Iterable[Norm]:
        """Iterator over all norms in the document."""
        iterator = self._dokumente.iter("norm")
        next(
            iterator
        )  # needed to skip the first norm, which is purely metadata for the dokument
        for norm in iterator:
            yield wrap_node(norm)

    def __call__(self, index: int) -> Norm:
        """Get a norm by index."""
        return self[index]

    def __getitem__(self, index: int) -> Norm:
        """Get a norm by index."""
        return wrap_node(self._dokumente.findall("norm")[index])

    @override
    def __str__(self) -> str:
        """The text content of the document."""
        return "\n".join([repr(norm) + "\n" + str(norm) for norm in self])

    @override
    def __repr__(self) -> str:
        """The full reference to the document."""
        return (
            self.langue
            or self.kurzue
            or self.amtabk
            or self.jurabk
            or super().__repr__()
        )

    def __len__(self) -> int:
        """The number of norms in the document."""
        return len(self._dokumente.findall("norm"))

    def get(self, dokument_url: str) -> bytes:
        """Get a dokuments data from the web."""
        self._url = dokument_url
        response = get(dokument_url)
        with ZipFile(BytesIO(response.content)) as zipdata:
            for zipped_file in zipdata.namelist():
                if zipped_file.endswith("xml"):
                    with zipdata.open(zipped_file) as book_file:
                        return book_file.read()
            raise BadDataError("zip file did not include a xml file")

    def parse(self, book_data: bytes) -> None:
        """Parse dokument data into this instance and validate if needed."""
        self._dokumente = etree.fromstring(book_data)

    def validate(self) -> None:
        """Validate this documents xml data."""
        tree = etree.ElementTree(self._dokumente)
        dtd_data = get(tree.docinfo.system_url).content
        dtd = etree.DTD(BytesIO(dtd_data))
        if not dtd.validate(tree):
            raise ValidationError(dtd.error_log.filter_from_errors()[0])

    @property
    def href(self) -> str:
        """The url under which the html version of this document can be found."""
        return self.URL_TEMPLATE % {
            "jurabk": replace_umlauts(self.jurabk.lower()) if self.jurabk else ""
        }

    @cached_property
    def _metadaten(self) -> etree._Element | None:
        return self._dokumente[0].find("metadaten")

    @cached_property
    def _textdaten(self) -> etree._Element | None:
        return self._dokumente[0].find("textdaten")

    @property
    def builddate(self) -> datetime | None:
        """The datetime the underlying xml was built."""
        builddate = self._dokumente.get("builddate")
        return (
            datetime.strptime(builddate, BUILDDATE_FORMAT).astimezone(TIMEZONE)
            if builddate
            else None
        )

    @property
    def doknr(self) -> str | None:
        """The document number of the underlying xml file."""
        return self._dokumente.get("doknr")

    @property
    def jurabk(self) -> str | None:
        """The common abbreviation of the document name ('Juristische Abkürzung')."""
        return self._metadaten.findtext("jurabk") if self._metadaten else None

    @property
    def amtabk(self) -> str | None:
        """The official abbreviation of the document name ('Amtliche Abkürzung')."""
        return self._metadaten.findtext("amtabk") if self._metadaten else None

    @property
    def kurzue(self) -> str | None:
        """The shortform of the full document name."""
        return self._metadaten.findtext("kurzue") if self._metadaten else None

    @property
    def langue(self) -> str | None:
        """The long form of the full document name."""
        return self._metadaten.findtext("langue") if self._metadaten else None

    @property
    def _ausfertigung(self) -> etree._Element | None:
        return self._metadaten.find("ausfertigung-datum") if self._metadaten else None

    @property
    def ausfertigung_datum(self) -> datetime | None:
        """The date this law was signed into effect."""
        if self._ausfertigung:
            text = self._ausfertigung.text
            if text:
                return datetime.strptime(text, "%Y-%m-%d").astimezone(TIMEZONE)
        return None

    @property
    def ausfertigung_manuell(self) -> bool | None:
        """Whether this law was signed manually."""
        if self._ausfertigung is not None:
            ausfertigung_manuell = self._ausfertigung.get("manuell")
            if ausfertigung_manuell is not None:
                return ausfertigung_manuell.lower() == "ja"
        return None

    @property
    def _fundstelle(self) -> etree._Element | None:
        return self._metadaten.find("fundstelle") if self._metadaten else None

    @property
    def fundstelle_typ(self) -> str | None:
        return self._fundstelle.get("typ") if self._fundstelle is not None else None

    @property
    def fundstelle_periodikum(self) -> str | None:
        return (
            self._fundstelle.findtext("periodikum")
            if self._fundstelle is not None
            else None
        )

    @property
    def fundstelle_zitstelle(self) -> str | None:
        return (
            self._fundstelle.findtext("zitstelle")
            if self._fundstelle is not None
            else None
        )

    @property
    def _standangabe(self) -> etree._Element | None:
        return self._metadaten.find("standangabe") if self._metadaten else None

    @property
    def standangabe_typ(self) -> str | None:
        return (
            self._standangabe.findtext("standtyp")
            if self._standangabe is not None
            else None
        )

    @property
    def standangabe_checked(self) -> bool | None:
        if self._standangabe is not None:
            standangabe_checked = self._standangabe.get("checked")
            if standangabe_checked is not None:
                return standangabe_checked.lower() == "ja"
        return None

    @property
    def standangabe_kommentar(self) -> str | None:
        return (
            self._standangabe.findtext("standkommentar")
            if self._standangabe is not None
            else None
        )

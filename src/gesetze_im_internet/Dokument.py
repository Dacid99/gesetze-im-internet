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

from gesetze_im_internet.constants import BUILDDATE_FORMAT, TIMEZONE, WEB_PROTOCOL
from gesetze_im_internet.exceptions import BadDataError, ValidationError
from gesetze_im_internet.utils import register, replace_umlauts, wrap_node


if TYPE_CHECKING:
    from collections.abc import Iterable

    from .Norm import Norm


@register
class Dokument:
    """A wrapper for a dokumente xml element."""

    _TAG = "dokumente"
    URL_TEMPLATE = WEB_PROTOCOL + "www.gesetze-im-internet.de/%(jurabk)s/index.html"

    def __init__(self, book_url: str | None = None, validate: bool = False) -> None:
        if book_url:
            self.parse(self.get(book_url), validate=validate)

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
        return wrap_node(self._tree.findall("norm")[index])

    def __str__(self) -> str:
        """The text content of the document."""
        return "\n".join([repr(norm) + "\n" + str(norm) for norm in self])

    def __repr__(self) -> str:
        """The full reference to the document."""
        return self.langue or self.kurzue or self.amtabk or self.jurabk

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

    def parse(self, book_data: bytes, validate: bool = False) -> None:
        """Parse dokument data into this instance and validate if needed."""
        self._tree = etree.parse(BytesIO(book_data))
        if validate:
            self.validate()

    def validate(self) -> None:
        """Validate this documents xml data."""
        dtd_data = self._get_dtd(self._tree.docinfo.system_url)
        dtd = etree.DTD(BytesIO(dtd_data))
        if not dtd.validate(self._tree):
            raise ValidationError(dtd.error_log.filter_from_errors()[0])

    def _get_dtd(self, dtd_url: str):
        response = get(dtd_url)
        return response.content

    @property
    def href(self) -> str:
        """The url under which the html version of this document can be found."""
        return self.URL_TEMPLATE % {"jurabk": replace_umlauts(self.jurabk.lower())}

    @cached_property
    def _dokumente(self):
        return self._tree.getroot()

    @cached_property
    def _metadaten(self):
        return self._dokumente[0].find("metadaten")

    @cached_property
    def _textdaten(self):
        return self._dokumente[0].find("textdaten")

    @property
    def builddate(self) -> datetime | None:
        """The datetime the underlying xml was built."""
        builddate = self._dokumente.attrib.get("builddate")
        return (
            datetime.strptime(builddate, BUILDDATE_FORMAT).astimezone(TIMEZONE)
            if builddate
            else None
        )

    @property
    def doknr(self) -> str | None:
        """The document number of the underlying xml file."""
        return self._dokumente.attrib.get("doknr")

    @property
    def jurabk(self) -> str | None:
        """The common abbreviation of the document name ('Juristische Abkürzung')."""
        return self._metadaten.findtext("jurabk")

    @property
    def amtabk(self) -> str | None:
        """The official abbreviation of the document name ('Amtliche Abkürzung')."""
        return self._metadaten.findtext("amtabk")

    @property
    def kurzue(self) -> str | None:
        """The shortform of the full document name."""
        return self._metadaten.findtext("kurzue")

    @property
    def langue(self) -> str | None:
        """The long form of the full document name."""
        return self._metadaten.findtext("langue")

    @property
    def ausfertigung_datum(self) -> datetime | None:
        """The date this law was signed into effect."""
        ausfertigung_datum = self._metadaten.findtext("ausfertigung-datum")
        return (
            datetime.strptime(ausfertigung_datum, "%Y-%m-%d").astimezone(TIMEZONE)
            if ausfertigung_datum
            else None
        )

    @property
    def ausfertigung_manuell(self) -> bool | None:
        """Whether this law was signed manually."""
        ausfertigung_datum = self._metadaten.find("ausfertigung-datum")
        return (
            ausfertigung_datum.attrib.get("manuell").lower() == "ja"
            if ausfertigung_datum is not None
            else None
        )

    @property
    def fundstelle_typ(self) -> str | None:
        fundstelle = self._metadaten.find("fundstelle")
        return fundstelle.attrib.get("typ") if fundstelle is not None else None

    @property
    def fundstelle_periodikum(self) -> str | None:
        fundstelle = self._metadaten.find("fundstelle")
        return fundstelle.findtext("periodikum") if fundstelle is not None else None

    @property
    def fundstelle_zitstelle(self) -> str | None:
        fundstelle = self._metadaten.find("fundstelle")
        return fundstelle.findtext("zitstelle") if fundstelle is not None else None

    @property
    def standangabe_typ(self) -> str | None:
        standangabe = self._metadaten.find("standangabe")
        return standangabe.findtext("standtyp") if standangabe is not None else None

    @property
    def standangabe_checked(self) -> str | None:
        standangabe = self._metadaten.find("standangabe")
        return (
            standangabe.attrib.get("checked").lower() == "ja"
            if standangabe is not None
            else None
        )

    @property
    def standangabe_kommentar(self) -> str | None:
        standangabe = self._metadaten.find("standangabe")
        return (
            standangabe.findtext("standkommentar") if standangabe is not None else None
        )

# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.


from collections.abc import Iterable
from datetime import datetime
from functools import cached_property
from io import BytesIO
from zipfile import ZipFile

from lxml import etree
from requests import get

from gesetze_im_internet.constants import BUILDDATE_FORMAT
from gesetze_im_internet.exceptions import ValidationError

from .Norm import Norm


class Dokument:
    def __init__(self, book_url: str | None = None, validate=False) -> None:
        if book_url:
            self.parse(self.get(book_url), validate=True)

    def __iter__(self) -> Iterable[str]:
        for norm in self._dokumente.iter("norm"):
            yield str(Norm(norm))

    def __call__(
        self,
    ) -> Norm:
        return Norm()

    def __str__(self) -> str:
        return self.langue or self.kurzue or self.amtabk or self.jurabk

    def get(self, book_url: str):
        self._url = book_url
        response = get(book_url)
        with ZipFile(BytesIO(response.content)) as zipdata:
            if len(zipdata.namelist()) == 1:
                with zipdata.open(zipdata.namelist()[0]) as book_file:
                    return book_file.read()

    def parse(self, book_data: bytes, validate: bool = False) -> None:
        self._tree = etree.parse(BytesIO(book_data))
        if validate:
            self._validate(self._tree)

    def _validate(self, tree: etree._ElementTree):
        dtd_data = self._get_dtd(self._tree.docinfo.system_url)
        dtd = etree.DTD(BytesIO(dtd_data))
        if not dtd.validate(self._tree):
            raise ValidationError(dtd.error_log.filter_from_errors()[0])

    def _get_dtd(self, dtd_url: str):
        response = get(dtd_url)
        return response.content

    @property
    def href(self) -> str:
        if hasattr(self, "_url"):
            return self._url.rsplit("/", maxsplit=1)[0] + "/index.html"
        raise ValueError("This Dokument has not read any online source yet.")

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
        builddate = self._dokumente.attrib.get("builddate")
        return datetime.strptime(builddate, BUILDDATE_FORMAT) if builddate else None

    @property
    def doknr(self) -> str | None:
        return self._dokumente.attrib.get("doknr")

    @property
    def jurabk(self) -> str | None:
        return self._metadaten.findtext("jurabk")

    @property
    def amtabk(self) -> str | None:
        return self._metadaten.findtext("amtabk")

    @property
    def kurzue(self) -> str | None:
        return self._metadaten.findtext("kurzue")

    @property
    def langue(self) -> str | None:
        return self._metadaten.findtext("langue")

    @property
    def ausfertigung_datum(self):
        ausfertigung_datum = self._metadaten.findtext("ausfertigung-datum")
        return (
            datetime.strptime(ausfertigung_datum, "%Y-%m-%d")
            if ausfertigung_datum
            else None
        )

    @property
    def ausfertigung_manuell(self):
        ausfertigung_datum = self._metadaten.find("ausfertigung-datum")
        return (
            ausfertigung_datum.attrib.get("manuell").lower() == "ja"
            if ausfertigung_datum is not None
            else None
        )

    @property
    def fundstelle_typ(self):
        fundstelle = self._metadaten.find("fundstelle")
        return fundstelle.attrib.get("typ") if fundstelle is not None else None

    @property
    def fundstelle_periodikum(self):
        fundstelle = self._metadaten.find("fundstelle")
        return fundstelle.attrib.get("periodikum") if fundstelle is not None else None

    @property
    def fundstelle_zitstelle(self):
        fundstelle = self._metadaten.find("fundstelle")
        return fundstelle.attrib.get("zitstelle") if fundstelle is not None else None

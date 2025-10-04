# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.


from zipfile import ZipFile
from io import BytesIO
from requests import get
from lxml import etree
from .Einheit import Einheit
from .Norm import Norm
from datetime import datetime
from gesetze_im_internet.exceptions import ValidationError
from typing import Iterable


class Dokument:
    class Metadata:
        class TextData:
            pass

        class Fundstelle:
            pass

        class StandAngabe:
            pass

    def __init__(self, book_url: str | None = None, validate=False) -> None:
        self._toc: dict[str, Norm | Einheit] = {}
        if book_url:
            self.parse(self.get(book_url), validate=True)

    def __iter__(self) -> Iterable[str]:
        return iter(self._toc.keys())

    def __str__(self) -> str:
        return self.langue

    def get(self, book_url: str):
        self._url = book_url
        response = get(book_url)
        with ZipFile(BytesIO(response.content)) as zipdata:
            if len(zipdata.namelist()) == 1:
                with zipdata.open(zipdata.namelist()[0]) as book_file:
                    return book_file.read()

    def parse(self, book_data: bytes, validate: bool = False) -> None:
        tree = etree.parse(BytesIO(book_data))
        if validate:
            self._validate(tree)
        dokumente = tree.getroot()
        self.builddate = datetime.strptime(
            dokumente.attrib.get("builddate"), "%Y%m%d%H%M%S"
        )
        self.doknr = dokumente.attrib.get("doknr")
        metadata = dokumente[0].find("metadaten")
        self.jurabk = metadata.find("jurabk").text
        self.amtabk = metadata.find("amtabk").text
        ausfertigung = metadata.find("ausfertigung-datum")
        self.ausfertigung_date = datetime.strptime(ausfertigung.text, "%Y-%m-%d")
        self.ausfertigung_manuell = ausfertigung.attrib.get("manuell").lower() == "ja"
        self.kurzue = metadata.find("kurzue").text
        self.langue = metadata.find("langue").text
        fundstelle = metadata.find("fundstelle")
        self.fundstelle_typ = fundstelle.attrib.get("amtlich")
        self.fundstelle_periodikum = fundstelle.find("periodikum").text
        self.fundstelle_zitstelle = fundstelle.find("zitstelle").text

    def _validate(self, tree: etree._ElementTree):
        dtd_data = self._get_dtd(tree.docinfo.system_url)
        dtd = etree.DTD(BytesIO(dtd_data))
        if not dtd.validate(tree):
            raise ValidationError(dtd.error_log.filter_from_errors()[0])

    def _get_dtd(self, dtd_url: str):
        response = get(dtd_url)
        return response.content

    def href(self):
        if hasattr(self, "_url"):
            return self._url.rsplit("/", maxsplit=1)[0] + "/index.html"
        raise ValueError("This Dokument has not read any online source yet.")

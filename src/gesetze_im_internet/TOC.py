# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

from lxml import etree
from requests import get

from gesetze_im_internet.exceptions import DownloadError

from .Dokument import Dokument


class TOC:
    URL = "https://www.gesetze-im-internet.de/gii-toc.xml"

    def __init__(self, toc_url: str = URL) -> None:
        self._dict = {}
        self.parse(self.get(toc_url))

    def __iter__(self):
        return iter(self._dict.keys())

    def __str__(self):
        return "Gesetze-im-Internet Inhaltsverzeichnis"

    def __repr__(self) -> str:
        return str(self)

    def __len__(self):
        return len(self._dict)

    def as_dict(self):
        return self._dict

    def __call__(self, title: str, validate: bool = False) -> Dokument:
        return Dokument(self._dict[title], validate=validate)

    def __getitem__(self, title: str) -> Dokument:
        return self(title, validate=False)

    def get(self, toc_url: str = URL) -> bytes:
        response = get(toc_url)
        if response.status_code == 200:
            return response.content
        raise DownloadError("Request for TOC did not return the expected data.")

    def parse(self, toc_data: bytes) -> None:
        items = etree.fromstring(toc_data)
        for item in items:
            title = item.find("title")
            if title is not None:
                self._dict[title.text] = item.find("link").text

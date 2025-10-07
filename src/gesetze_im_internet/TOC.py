# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

from collections.abc import Iterator

from lxml import etree
from requests import codes, get
from typing_extensions import override

from gesetze_im_internet.exceptions import DownloadError

from .Dokument import Dokument


class TOC:
    """The wrapper for the xml toc data."""

    URL = "https://www.gesetze-im-internet.de/gii-toc.xml"

    @override
    def __init__(self, toc_url: str = URL) -> None:
        self._dict = {}
        self.parse(self.get(toc_url))

    def __iter__(self) -> Iterator[str]:
        """Iterator over the document in the toc."""
        return iter(self._dict.keys())

    @override
    def __str__(self) -> str:
        """The name of the toc."""
        return "Gesetze-im-Internet Inhaltsverzeichnis"

    @override
    def __repr__(self) -> str:
        """The name of the toc."""
        return str(self)

    def __len__(self) -> int:
        """The number of document in the toc."""
        return len(self._dict)

    def __call__(self, title: str, validate: bool = False) -> Dokument:
        """Get a document by title and validate it if needed."""
        return Dokument(self._dict[title], validate=validate)

    def __getitem__(self, title: str) -> Dokument:
        """Get a document by title."""
        return self(title, validate=False)

    def get(self, toc_url: str = URL) -> bytes:
        """Get the toc data from the web."""
        response = get(toc_url)
        if response.status_code == codes.ok:
            return response.content
        raise DownloadError("Request for TOC did not return the expected data.")

    def parse(self, toc_data: bytes) -> None:
        """Parse the toc data into this instance."""
        items = etree.fromstring(toc_data)
        for item in items:
            title = item.find("title")
            if title is not None:
                self._dict[title.text] = item.findtext("link")

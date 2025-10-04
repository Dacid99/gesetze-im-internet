# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

from requests import get
from lxml import etree
from Book import Book


class TOC:
    URL = "https://www.gesetze-im-internet.de/gii-toc.xml"

    def __init__(self) -> None:
        self.dict = {}

    def __iter__(self):
        return self.titles

    def __call__(self, title, validate=False) -> Book:
        return Book(self.dict[title], validate=validate)

    def get(self, toc_url=URL):
        response = get(toc_url)
        if response.status_code == 200:
            return response.content

    def parse(self, toc_data):
        root = etree.fromstring(toc_data)

        for item in root:
            title = item.find("title")
            if title:
                self.dict[title.text.decode()] = item.find("link").text.decode()

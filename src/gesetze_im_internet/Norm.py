# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

import re
from datetime import datetime
from functools import cached_property

from gesetze_im_internet.constants import BUILDDATE_FORMAT
from gesetze_im_internet.exceptions import ImproperTag

from .Absatz import Absatz


class Norm:
    def __init__(self, norm_node) -> None:
        if norm_node.tag != "norm":
            raise ImproperTag()
        self._norm_node = norm_node

    def __iter__(self) -> int:
        for absatz_node in self._norm_node.iterfind(".//P"):
            yield int(Absatz(absatz_node))

    def __call__(self, absatz_nr) -> Absatz:
        return Absatz()

    def __str__(self) -> str:
        return self.jurabk + self.enbez + ": " + self.title

    def __int__(self) -> int:
        return self.nr or 0

    @property
    def href(self) -> str:
        if hasattr(self, "_url"):
            return self._url.rsplit("/", maxsplit=1)[0] + "/index.html"

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
    def enbez(self) -> str | None:
        return self._metadaten.findtext("enbez")

    @property
    def titel(self) -> str | None:
        return self._metadata.findtext("titel")

    @property
    def titel_format(self) -> str | None:
        return self._metadata.find("titel").attrib.get("format")

    @property
    def nr(self) -> int | None:
        if self.enbez:
            nr_match = re.match(r"(\d+)", self.enbez)
            if nr_match:
                return int(nr_match.group(1))
        return None

# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

from datetime import datetime


class Norm:
    class Metadata:
        pass

    class Textdata:
        class Fussnoten:
            pass

    def __init__(self, norm_node) -> None:
        self.builddate = datetime.strptime(
            norm_node.attrib.get("builddate"), "%Y%m%d%H%M%S"
        )
        self.doknr = norm_node.attrib.get("doknr")
        metadata = norm_node.find("metadaten")
        self.enbez = metadata.find("enbez").text
        self.jurabk = metadata.find("jurabk").text
        textdata = norm_node.find("textdaten")
        self.title = textdata.find("titel").text
        self.title_format = norm_node.find("textdaten").find("titel").text

    def __str__(self):
        return self.enbez + ": " + self.title

    def href(self):
        if hasattr(self, "_url"):
            return self._url.rsplit("/", maxsplit=1)[0] + "/index.html"
        raise ValueError("This Dokument has not read any online source yet.")

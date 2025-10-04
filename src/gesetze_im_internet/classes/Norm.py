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
    def __init__(self, norm_node) -> None:
        self.builddate = datetime.strptime(
            norm_node.attrib["builddate"].decode(), "%Y%m%d%H%M%S"
        )
        self.doknr = norm_node.attrib["doknr"]
        metadata = norm_node.find("metadaten")
        self.enbez = metadata.find("enbez").text.decode()
        self.jurabk = metadata.find("jurabk").text.decode()
        textdata = norm_node.find("textdaten")
        self.title = textdata.find("titel").text.decode()
        self.title_format = norm_node.find("textdaten").find("titel").text.decode()

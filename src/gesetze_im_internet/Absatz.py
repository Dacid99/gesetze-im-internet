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

from gesetze_im_internet.exceptions import ImproperTag

from .Norm import Norm


class Absatz:
    NR_REGEX = r"^\s*\(\s*(\d+)\s*\)"

    def __init__(self, absatz_node) -> None:
        if absatz_node.tag != "P":
            raise ImproperTag()
        self._absatz_node = absatz_node

    def __int__(self) -> int:
        return self.nr or 0

    def __str__(self) -> str:
        return str(self.norm) + (str(self.nr) if self.nr else "")

    @property
    def text(self) -> str:
        return re.sub(self.NR_REGEX, "", self._absatz_node.text, count=0).strip()

    @property
    def sätze(self) -> str:
        return self.text.split(". ")

    @property
    def nr(self) -> int | None:
        nr_match = re.match(self.NR_REGEX, self._absatz_node.text)
        return int(nr_match.group(1)) if nr_match else None

    @property
    def norm(self) -> Norm:
        norm_candidate = self._absatz_node.getparent()
        while norm_candidate.tag != "norm":
            norm_candidate = self.absatz_node.getparent()
        return Norm(norm_candidate)

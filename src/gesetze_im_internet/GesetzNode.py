# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

from abc import ABC

from lxml import etree

from gesetze_im_internet.exceptions import ImproperTagError


class GesetzNode(ABC):
    TAG = ""

    def __init__(self, node: etree._Element) -> None:
        if node.tag != self.TAG:
            raise ImproperTagError
        self._node = node

    def __bytes__(self) -> bytes:
        """Get the raw binary xml of the node."""
        return etree.tostring(self._node)

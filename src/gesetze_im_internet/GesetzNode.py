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
        return etree.tostring(self._node)

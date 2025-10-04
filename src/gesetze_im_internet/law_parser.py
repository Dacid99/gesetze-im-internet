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
from datetime import datetime

def parse_toc(toc_data):
    root = etree.fromstring(toc_data)

    print(root.tag)
    for child in root:
        if child[0].tag == "title":
            print(child[0].text)
        if child[1].tag == "link":
            print(child[1].text.replace("http://", "https://"))


def parse_book(book_data):
    root = etree.fromstring(book_data)

    print(root.tag)
    for child in root:
        parse_norm(child)


def parse_norm(norm_node: etree.ElementBase):
    builddate = norm_node.attrib.get("builddate")
    builddatetime = datetime(year=builddate[0:2], month=builddate[2:4], day=builddate[4:6], hour=builddate[6:8], minute=builddate[8:10], second=builddate[10:12])
    doknr = norm_node.attrib.get("doknr")
    parse_norm_metadata(norm_node.find("metadaten"))
    parse_norm_textdata(norm_node.find("textdaten"))


def parse_norm_metadata(metadata_node):
    enbez = metadata_node.find("enbez")
    titel = metadata_node.find("titel")


def parse_norm_textdata(textdata_node):
    text = textdata_node.find("text")
    if text.attrib.get("format") == "XML":
        content = text.find("content")


def parse_norm_content(node_content):
    for child in node_content:
        if child.tag == "P":
            absatz = child
            alternativen = absatz.find("DL")
            if alternativen:
                for child in alternativen:
                    parse_alternative(child)

def parse_alternative(alternative):
    alternative.


def validate_book(book_data):
    dtd = etree.DTD(book_data)

    dtd.validate(book_data)

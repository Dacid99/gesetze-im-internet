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


def test_Dokument_from_TOC(toc):
    dokument = toc("Handelsgesetzbuch", validate=True)

    assert dokument.jurabk == "HGB"
    assert dokument.langue == "Handelsgesetzbuch"
    assert len(dokument)
    assert list(dokument)
    assert str(dokument)
    assert repr(dokument)
    assert dokument.href.startswith("https://www.gesetze-im-internet.de/")
    assert isinstance(dokument.builddate, datetime)
    assert dokument.builddate.tzinfo
    assert isinstance(dokument.ausfertigung_datum, datetime)
    assert dokument.builddate.tzinfo
    assert dokument.doknr
    assert dokument.fundstelle_typ
    assert dokument.fundstelle_periodikum
    assert dokument.fundstelle_zitstelle
    assert dokument.standangabe_typ
    assert dokument.standangabe_kommentar

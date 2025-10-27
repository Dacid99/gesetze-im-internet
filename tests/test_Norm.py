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


def test_Norm_Gesetz(toc):
    norm = toc("Strafgesetzbuch")[11]

    assert str(norm)
    assert len(norm)
    assert list(norm)
    assert int(norm)
    assert repr(norm)
    assert not norm.is_gliederung
    assert norm.nr
    assert norm.dokument
    assert norm.enbez
    assert norm.jurabk
    assert norm.doknr
    assert norm.href.startswith("https://www.gesetze-im-internet.de/")
    assert isinstance(norm.builddate, datetime)
    assert norm.builddate.tzinfo
    assert norm.titel


def test_Norm_Gliederung(toc):
    norm = toc("Verwaltungsverfahrensgesetz")[2]

    assert str(norm)
    assert len(norm)
    assert list(norm)
    assert int(norm)
    assert repr(norm)
    assert norm.is_gliederung
    assert norm.dokument
    assert norm.gliederungskennzahl
    assert norm.gliederungsbez
    assert norm.gliederungstitel
    assert norm.jurabk
    assert norm.doknr
    assert norm.href.startswith("https://www.gesetze-im-internet.de/")
    assert isinstance(norm.builddate, datetime)
    assert norm.builddate.tzinfo

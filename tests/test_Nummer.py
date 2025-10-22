# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.


def test_Nummer(toc):
    book = toc("Gerichtsverfassungsgesetz")
    norm = book[38]
    absatz = norm[0]
    satz = absatz[0]
    nummer = satz[1]

    assert int(nummer)
    assert str(nummer)
    assert repr(nummer)
    assert nummer.nr

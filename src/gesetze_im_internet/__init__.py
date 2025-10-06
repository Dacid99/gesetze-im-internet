# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.


from .Absatz import Absatz
from .Dokument import Dokument
from .Norm import Norm
from .TOC import TOC


__all__ = ["TOC", "Absatz", "Alternative", "Dokument", "Norm", "Nummer", "Satz"]

toc = TOC()

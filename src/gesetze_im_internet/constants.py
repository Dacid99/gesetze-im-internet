# SPDX-License-Identifier: EUPL-1.1
# Copyright (C) 2025 David Aderbauer
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the European Union Public License Version 1.1 as
# published by the European Union.
#
# You should have received a copy of the European Union Public License Version 1.1
# along with this program. If not, see <https://spdx.org/licenses/>.

from zoneinfo import ZoneInfo


WEB_PROTOCOL = "https://"

TOC_URL = WEB_PROTOCOL + "www.gesetze-im-internet.de/gii-toc.xml"


BUILDDATE_FORMAT = "%Y%m%d%H%M%S"

TIMEZONE = ZoneInfo("Europe/Berlin")

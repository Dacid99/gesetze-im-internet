# Gesetze-Im-Internet Python Package

![PyPI - Downloads](https://img.shields.io/pypi/dm/gesetze-im-internet)
![PyPI - Version](https://img.shields.io/pypi/v/gesetze-im-internet)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/gesetze-im-internet)
![PyPI - License](https://img.shields.io/pypi/l/gesetze-im-internet)
![Coverage](https://gitlab.com/Dacid99/gesetze-im-internet/badges/master/coverage.svg?job=test_codebase)
![Pipeline](https://gitlab.com/Dacid99/gesetze-im-internet/badges/master/pipeline.svg)

## A simple API to access data from gesetze-im-internet.de

www.gesetze-im-internet.de offers an xml version of the laws for access by third parties.
The xml toc can be found at https://www.gesetze-im-internet.de/gii-toc.xml, the links in it point to the various legal documents.

This package uses this feature to provide access to the individual laws, books, etc.

### Installation

Install from pypi

```bash
pip install gesetze-im-internet
```

or compile yourself

```bash
git clone https://gitlab.com/Dacid99/gesetze-im-internet.git
pip install poetry
poetry install
```

### License

This software is licensed under the European Union Public License Version 1.1 . This a copyleft open-source license explicitly compatible with the GPL licenses, designed for legal security throughout the European Union member states.

## Basic Usage

### Table of Contents

Import the gesetze-im-internet table of contents to get access to the entire library

```python
from gesetze_im_internet import toc
```

This object is your starting point for browsing and access all available law documents.
For example:

```python
>>> toc
Gesetze-im-Internet Inhaltsverzeichnis

>>> len(toc)
6450

>>> list(toc)
['Gesetz über die Ausprägung einer 1-DM-Goldmünze und die Errichtung der Stiftung "Geld und Währung"',
 'Erstes Gesetz zur Vereinheitlichung und Neuregelung des Besoldungsrechts in Bund und Ländern',
 ... ]

>>> toc[0]
Gesetz über die Ausprägung einer 1-DM-Goldmünze und die Errichtung der Stiftung "Geld und Währung"

>>> toc("Bürgerliches Gesetzbuch", validate=True)
Bürgerliches Gesetzbuch
```

With the Dokument object you get from indexing or calling the toc, you now have a complete law book at your disposal.
All data is readonly. For complete information check out the source code either manually or with your favorite IDE's features.

```python
bgb = toc("Bürgerliches Gesetzbuch")

>>> bgb
Bürgerliches Gesetzbuch

>>> str(bgb)


>>> len(bgb)
2831

>>> list(bgb)
["BGB Inhaltsübersicht",
 "BGB Buch 1 Allgemeiner Teil",
 "BGB Abschnitt 1 Personen",
 "BGB Titel 1 Natürliche Personen, Verbraucher, Unternehmer",
 "BGB § 1 Beginn der Rechtsfähigkeit",
 ... ]

>>> for norm in bgb:
...     print(norm)
BGB Inhaltsübersicht
BGB Buch 1 Allgemeiner Teil
BGB Abschnitt 1 Personen
BGB Titel 1 Natürliche Personen, Verbraucher, Unternehmer
BGB § 1 Beginn der Rechtsfähigkeit
...

>>> bgb[5]
BGB § 1 Beginn der Rechtsfähigkeit

>>> bgb(1)
BGB § 1 Beginn der Rechtsfähigkeit

>>> bgb.href
'https://www.gesetze-im-internet.de/bgb/index.html'

>>> bgb.ausfertigung_datum
datetime.datetime(1896, 8, 18, 0, 0, tzinfo=zoneinfo.ZoneInfo(key='Europe/Berlin'))

>>> bgb.standangabe_kommentar
"Neugefasst durch Bek. v. 2.1.2002 I 42, 2909; 2003, 738;"

>>> bgb.builddate
datetime.datetime(2025, 7, 22, 21, 55, 7, tzinfo=zoneinfo.ZoneInfo(key='Europe/Berlin'))
```

Iterating the Dokument instance yields Norm instances, holding the data of individual laws.
You can access that data in a similar way.

```python
>>> abschnitt = bgb[2]

>>> abschnitt
BGB Buch 1 Allgemeiner Teil

>>> abschnitt.is_gliederung
True

>>> abschnitt.gliederungsbez
Buch 1

>>> paragraph1 = bgb[5]
# The Dokument class also holds norms encoding gliederungsüberschriften.
# Therefore the indexes and paragraph numbers do not necessarily align.

>>> paragraph1 = bgb(1)

>>> paragraph1.is_gliederung
False

>>> paragraph1.nr
1.0

>>> int(paragraph1)
1

>>> float(paragraph1)
# This returns an float version of the alphanumeric notation (3b -> 3.02).
# To translate this you can use gesetze_im_internet.utils.float2alphanumeric
1.0

>>> paragraph1.href
'https://www.gesetze-im-internet.de/bgb/__1.html'

>>> for absatz in paragraph1:
...     print(absatz)
(1) Die Rechtsfähigkeit des Menschen beginnt mit der Vollendung der Geburt.

>>> paragraph1
'BGB § 1 Beginn der Rechtsfähigkeit'

>>> str(paragraph1)
(1) Die Rechtsfähigkeit des Menschen beginnt mit der Vollendung der Geburt.

>>> len(paragraph1)
1

>>> list(paragraph1)
[BGB § 1 Beginn der Rechtsfähigkeit I]

>>> bytes(paragraph1)
b'<norm builddate="20251013215507" doknr="BJNR001950896BJNE000102377"><metadaten><jurabk>BGB</jurabk><enbez>&#167; 1</enbez><titel format="parat">Beginn der Rechtsf&#228;higkeit ..."

>>> paragraph1.titel
'Beginn der Rechtsfähigkeit'

>>> paragraph1.enbez
'§ 1'

>>> paragraph1[0]
BGB § 1 Beginn der Rechtsfähigkeit Abs. 1
# If you prefer to use roman notation for Absätze,
# the helper *gesetze_im_internet.utils.int2roman* converts integers to that notation.

>>> paragraph1(1)
BGB § 1 Beginn der Rechtsfähigkeit Abs. 1

>>> paragraph1.dokument
Bürgerliches Gesetzbuch
```

In the same fashion that a document is split into norms, a norm is split in absätze, an absatz is made of sätze and a satz may have nummern.
Please be aware that the logic for splitting into sätze is experimental and may yield faulty results.

Due to the complexity of the german language, further division into alternativen was not possible within the scope of this project.

## Contributing

Everyone is invited to contribute to this project!

Just contact me or send me a merge request on [gitlab](https://gitlab.com/Dacid99/gesetze-im-internet).

Please make sure to read [the contributing guideline](CONTRIBUTING.md) and [the development guide](DEVELOPMENT.md) to get a headstart

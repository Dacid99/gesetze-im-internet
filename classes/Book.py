from zipfile import ZipFile
from io import BytesIO
from requests import get
from lxml import etree
from Einheit import Einheit
from datetime import datetime

class Book:
    def __init__(self, book_url: str|None = None, validate=False):
        self.einheiten: dict[str,Einheit] = {}
        if book_url:
            self.parse(self.get(book_url))

    def get(self, book_url):
        response = get(book_url) 
        with ZipFile(BytesIO(response.content)) as zipdata:
            if len(zipdata.namelist()) == 1:
                with zipdata.open(zipdata.namelist()[0]) as book_file:
                    return book_file.read()
            
    def parse(self, book_data):
        dokumente = etree.fromstring(book_data)
        self.builddate = datetime.strptime(dokumente.attrib["builddate"].decode(), "%Y-%m-%d")
        self.doknr = dokumente.attrib["doknr"]
        metadata = dokumente[0].find("metadaten") 
        self.jurabk = metadata.find("jurabk").text.decode()
        ausfertigung = metadata.find("ausfertigung-datum")
        self.ausfertigung_date = ausfertigung.text.decode()
        self.ausfertigung_manuell = ausfertigung.attrib["manuell"].lower() == "ja"
        self.langue = metadata.find("langue").text.decode()
        fundstelle = metadata.find("fundstelle")
        self.fundstelle_typ = fundstelle.attrib["amtlich"]
        self.fundstelle_periodikum = fundstelle.find("periodikum").text.decode()
        self.fundstelle_zitstelle = fundstelle.find("zitstelle").text.decode()
    
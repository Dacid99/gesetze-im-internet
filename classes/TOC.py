from typing import Any
from requests import get
from lxml import etree
from Book import Book

class TOC:

    URL = "https://www.gesetze-im-internet.de/gii-toc.xml"

    def __init__(self) -> None:
        self.dict = {}
    
    def __iter__(self):
        return self.titles
    
    def __call__(self, title, validate=False) -> Book:
        return Book(self.dict[title], validate=validate)


    def get(self, toc_url = URL):
        response = get(toc_url)
        if response.status_code == 200:
            return response.content
        
    def parse(self, toc_data):
        root = etree.fromstring(toc_data)

        for item in root:
            title = item.find("title")
            if title:
                self.dict[title.text.decode()] = item.find("link").text.decode()


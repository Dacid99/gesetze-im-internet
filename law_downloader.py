from requests import get
from constants import TOC_URL
from zipfile import ZipFile
from io import BytesIO


def get_toc():
    response = get(TOC_URL)
    if response.status_code == 200:
        return response.content
    return None


def get_norm_dtd(dtd_url):
    response = get(dtd_url)
    if response.status_code == 200:
        return response.content
    return None


def get_book(book_url):
    response = get(book_url) 
    with ZipFile(BytesIO(response.content)) as zipdata:
        if len(zipdata.namelist()) == 1:
            with zipdata.open(zipdata.namelist()[0]) as book_file:
                return book_file.read()

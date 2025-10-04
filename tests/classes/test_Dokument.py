from gesetze_im_internet.classes import TOC


def test_Dokument_from_TOC():
    toc = TOC()
    dokument = toc("Handelsgesetzbuch", validate=True)

    assert dokument.jurabk == "HGB"
    assert dokument.langue == "Handelsgesetzbuch"
    assert isinstance(dokument.einheiten, list)

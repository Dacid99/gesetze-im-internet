from gesetze_im_internet.classes import TOC


def test_TOC():
    toc = TOC()

    assert "Bürgerliches Gesetzbuch" in list(toc)

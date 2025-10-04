from datetime import datetime

class Norm:
    def __init__(self, norm_node) -> None:
        self.builddate = datetime.strptime(norm_node.attrib["builddate"].decode(), "%Y%m%d%H%M%S")
        self.doknr = norm_node.attrib["doknr"]
        metadata= norm_node.find("metadaten")
        self.enbez = metadata.find("enbez").text.decode()
        self.jurabk = metadata.find("jurabk").text.decode()
        textdata = norm_node.find("textdaten")
        self.title = textdata.find("titel").text.decode()
        self.title_format = norm_node.find("textdaten").find("titel").text.decode()


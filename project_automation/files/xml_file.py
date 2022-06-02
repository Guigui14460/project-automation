from typing import NoReturn
import defusedxml.minidom
import xml.etree.ElementTree as ET

from project_automation.files import CustomFileExtension


class XMLFile(CustomFileExtension):
    """
    Represents a `.xml` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "xml",
        "xml_tostring": {
            "encoding": "utf-8",
        },
        "indentation": "  ",
        "doctype": None,
    }

    def __init__(self, path: str, filename: str) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the file (not add the filename)
        filename : str
            name of the file without extension
        """
        super().__init__(path, filename)

    def init(self) -> NoReturn:
        """
        Initialize the content of the file.
        """
        self.root = ET.Element("root")
        ET.SubElement(self.root, "data")
        title = ET.SubElement(self.root, "h1")
        test1 = ET.SubElement(title, "test1")
        test1.set("myKey", "myValue")
        test1.set("emptyKey", "")
        ET.SubElement(title, "test1")
        self.write_xml()

    def append(self, string: str) -> NoReturn:
        """
        Append a string at correct place into the XML file.

        Parameters
        ----------
        string : str
            string to append
        """
        raise NotImplementedError

    def write_xml(self) -> NoReturn:
        """
        Write correctly the file in the XML format.
        """
        dom = self.prettify(self.root, doctype=self.CONFIG['doctype'])
        with open(self.filename, "w+") as f:
            f.write(dom)

    @classmethod
    def prettify(cls, elem: ET.Element, doctype: str = None) -> str:
        """
        Generate a pretty-printed XML string for the element.

        Parameters
        ----------
        elem : ~xml.etree.ElementTree.Element)
            the root element
        doctype : str
            the string to add before the root

        Returns
        -------
        string : str
            the all root in string format
        """
        data = ET.tostring(elem, **cls.CONFIG['xml_tostring'])
        dom = defusedxml.minidom.parseString(data)
        string = dom.toprettyxml(cls.CONFIG['indentation'])
        if doctype is not None:
            lines = string.split("\n")
            lines[0] = doctype
            string = "\n".join(lines)
        return string

from typing import NoReturn

from project_automation.files.xml_file import XMLFile, ET
from project_automation.utils import create_css_rule, common_prefix


class HTMLFile(XMLFile):
    """
    Represents a `.html` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG_HTML = {
        "extension": "html",
        "doctype": "<!DOCTYPE html>",
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
        self.CONFIG.update(self.CONFIG_HTML)
        super().__init__(path, filename)

    def init(self) -> NoReturn:
        """
        Initialize the content of the file.
        """
        self.root = ET.Element("html", attrib={"lang": "en"})
        self.head = ET.SubElement(self.root, "head")

        # Generic meta tags
        self.head.append(ET.Comment(text="Generic meta tags"))
        ET.SubElement(self.head, "meta", attrib={"charset": "UTF-8"})
        self.add_meta(
            content="width=device-width, initial-scale=1.0", name="viewport")
        self.add_meta(content="Document title", name="title")
        self.add_meta(content="Description of the document",
                      name="description")

        # Meta tags to index the site
        self.head.append(ET.Comment(text="Meta tags to index the website"))
        self.add_meta(content="", name="keywords")
        self.add_meta(content="index, follow", name="robots")
        self.add_meta(content="English", name="language")
        self.add_meta(content="5 days", name="revisit-after")

        # Meta tags for the social networks
        self.head.append(ET.Comment(
            "Meta tags to properly share website on the social networks"))
        self.head.append(ET.Comment("Meta tags for Open Graph from Facebook"))
        self.add_meta(content="website", property="og:type")
        self.add_meta(content="localhost:8000/index.html", property="og:url")
        self.add_meta(content="Document title", property="og:title")
        self.add_meta(content="Description of the document",
                      property="og:description")
        self.add_meta(
            content="https://metatags.io/assets/meta-tags-16a33a6a8531e519cc0936fbba0ad904e52d35f34a46c97a2c9f6f7dd7d336f2.png", property="og:image")
        self.head.append(ET.Comment("Meta tags for Twitter"))
        self.add_meta(content="summary_large_image", property="twitter:card")
        self.add_meta(content="localhost:8000/index.html",
                      property="twitter:url")
        self.add_meta(content="Document title", property="twitter:title")
        self.add_meta(content="Description of the document",
                      property="twitter:description")
        self.add_meta(
            content="https://metatags.io/assets/meta-tags-16a33a6a8531e519cc0936fbba0ad904e52d35f34a46c97a2c9f6f7dd7d336f2.png", property="twitter:image")

        self.title = ET.SubElement(self.head, "title")
        self.title.text = "Document title"

        self.body = ET.SubElement(self.root, "body")
        self.main_title = ET.SubElement(self.body, "h1")
        self.main_title.text = "Hello World"
        self.write_xml()

    def add_meta(self, content: str, name: str = None, property: str = None) -> NoReturn:
        """
        Add meta tag in the head of the HTML file.
        You must choice between `name` attribute and `property` attribute.

        Parameters
        ----------
        content : str
            ``content`` attribute of the meta tag
        name : str
            ``name`` attribute of the meta tag
        property : str
            ``property`` attribute of the meta tag
        """
        if (name is None and property is None) or (name is not None and property is not None):
            return
        dicte = {}
        if name is not None:
            dicte["name"] = name
        else:
            dicte["property"] = property
        dicte.update({"content": content})
        ET.SubElement(self.head, "meta", attrib=dicte)
        self.write_xml()

    def add_headlink(self, type: str, rel: str, href: str, href_is_relative: bool = True) -> NoReturn:
        """
        Add link tag in the head of the HTML file.

        Parameters
        ----------
        type : str
            ``type`` attribute of the meta tag
        rel : str
            ``rel`` attribute of the meta tag
        href : str
            ``href`` attribute of the meta tag
        href_is_relative : bool
            True if `href` is a relative path, False otherwise

        See also
        --------
        utils.common_prefix
        """
        if not href_is_relative:
            href = href.replace(common_prefix(
                [href, self.filename]), ".").replace("\\", "/")
        attrib = {"type": type, "rel": rel, "href": href}
        ET.SubElement(self.head, "link", attrib=attrib)
        self.write_xml()

    def add_style(self, rules: dict) -> NoReturn:
        """
        Add style tag into the file at the end of the head tag.

        Parameters
        ----------
        rules : dict
            dictionnary of rules (each rule is another dict with selector and properties keys)

        See also
        --------
        utils.create_css_rule
        """
        styles_to_add = ""
        for rule in rules:
            styles_to_add += create_css_rule(*rules[rule])
        style_tag = ET.SubElement(self.head, "style")
        style_tag.text = styles_to_add
        self.write_xml()

    def add_script(self, src: str, src_is_relative: bool = True) -> NoReturn:
        """
        Add script file into the body element.

        Parameters
        ----------
        src : str
            relative path of the file
        src_is_relative : bool
            True if `src` is a relative path, False otherwise

        See also
        --------
        utils.common_prefix
        """
        if not src_is_relative:
            src = src.replace(common_prefix(
                [src, self.filename]), ".").replace("\\", "/")
        script = ET.SubElement(self.body, "script", attrib={"src": src})
        script.text = " "
        self.write_xml()

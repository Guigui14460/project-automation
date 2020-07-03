from typing import NoReturn

from project_automation.files import CustomFileExtension
from project_automation.utils import create_css_rule


class CSSFile(CustomFileExtension):
    """
    Represents a `.css` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "css"
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
        self.append(self.create_rule(
            ["*", "*::after", "*::before"], {"box-sizing": "border-box"}))
        self.append(self.create_rule(["body"], {"margin": 0, "padding": 0}))

    def create_rule(self, selectors: list, properties: dict) -> str:
        """
        Return CSS rule properly formated.

        Parameters
        ----------
        selectors : list of string
            list of the CSS selector to apply all the properties
        properties : dict
            dictionnary of CSS properties to apply

        Returns
        -------
        rule : string
            pretty-printed CSS rule

        See also
        --------
        utils.create_css_rule
        """
        return create_css_rule(selectors, properties)

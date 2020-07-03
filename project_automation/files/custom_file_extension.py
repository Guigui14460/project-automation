import os
from typing import NoReturn

from project_automation.files import File


class CustomFileExtension(File):
    """Represents a custom extension file.

    Attributes
    ----------
    filename : str
        name of the file without extension
    """

    CONFIG = {
        "extension": ""
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
        File.__init__(self, os.path.join(
            path, f"{filename}.{self.CONFIG['extension']}"))
        self.init()

    def init(self) -> NoReturn:
        """
        Initialize the content of the file.
        """
        pass

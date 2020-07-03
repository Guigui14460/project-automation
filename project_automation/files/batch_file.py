import os
import stat
from typing import NoReturn

from project_automation.files import CustomFileExtension


class BatchFile(CustomFileExtension):
    """
    Represents a `.bat` file (format for Windows).

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "bat"
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
        content = "echo \"Hello World\""
        self.write(content)

    def write(self, string: str) -> NoReturn:
        """
        Write into the file.

        Parameters
        ----------
        string : str
            string to write into the file
        """
        super().write(string)
        os.chmod(self.filename, stat.S_IRWXU)

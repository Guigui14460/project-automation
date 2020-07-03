import os
from typing import NoReturn

from project_automation.files import CustomFileExtension


class CHeaderFile(CustomFileExtension):
    """
    Represents a `.h` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "h"
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
        content = f"""#ifndef {os.path.basename(self.filename).split('.')[0].upper()}_H
#define {os.path.basename(self.filename).split('.')[0].upper()}_H

int function(int, int);

#endif
"""
        self.write(content)

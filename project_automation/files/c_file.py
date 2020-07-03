import os
from typing import NoReturn

from project_automation.files import CustomFileExtension


class CFile(CustomFileExtension):
    """
    Represents a `.c` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "c"
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
        content = f"""#include "{os.path.basename(self.filename).split('.')[0].lower()}.h"

int function(int a, int b){{
    return a + b - 2;
}}
"""
        self.write(content)

    def init_main(self, other_file=None) -> NoReturn:
        """
        Initialize the content of the main file.

        Parameters
        ----------
        other_file : CFile
            other file to include in the top of the main file

        Raises
        ------
        TypeError
            when the other_file parameter is not a CFile instance
        """
        if not isinstance(other_file, CFile):
            raise TypeError("other_file must be another CFile object")
        include_other_file = f"#include \"{os.path.basename(other_file.filename).split('.')[0].lower()}.h\"" if other_file is not None else ""
        content = f"""#include <stdio.h>
{include_other_file}

int main(void){{
    int y = function(2,2);
    printf("%d\\n", y);
    return 0;
}}
"""
        self.write(content)

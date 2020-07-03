import os
from typing import NoReturn

from project_automation.files.c_file import CFile


class CPPFile(CFile):
    """
    Represents a `.cpp` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "cpp"
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

    def init_main(self, other_file=None, extension: str = 'h') -> NoReturn:
        """
        Initialize the content of the main file.

        Parameters
        ----------
        other_file : CFile
            other file to include in the top of the main file
        extension : str
            extension of the header file

        Raises
        ------
        TypeError
            when the other_file parameter is not a CPPFile instance
        """
        if not isinstance(other_file, CFile) and not isinstance(other_file, CPPFile):
            raise TypeError("other_file must be another CFile/CPPFile object")
        include_other_file = f"#include \"{os.path.basename(other_file.filename).split('.')[0].lower()}.{extension}\"" if other_file is not None else ""
        content = f"""#include <iostream>
{include_other_file}

int main(int argc, char const *argv[]) {{
    std::cout << "Hello World : " << function(2,-1) << std::endl;
    return 0;
}}
"""
        self.write(content)

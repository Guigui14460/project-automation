from typing import NoReturn

from project_automation.files.python_file import PythonFile


class CythonHeaderFile(PythonFile):
    """
    Represents a `.pxd` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "pxd"
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
        content = "cpdef int cython_function(int, int)"
        self.write(content)

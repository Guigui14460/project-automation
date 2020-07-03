from typing import NoReturn

from project_automation.files.python_file import PythonFile


class CythonFile(PythonFile):
    """
    Represents a `.pyx` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "pyx"
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
        content = """cpdef int cython_function(int a, int b):
    cdef int d = a * b
    return d ** 2
"""
        self.write(content)

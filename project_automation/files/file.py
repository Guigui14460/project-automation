import os
from typing import NoReturn


class File:
    """
    Represents a single file with base operations.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    def __init__(self, filename: str) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        filename : str
            represents the path of the file and his name (with the extension)
        """
        self.filename = filename
        self.create()

    def create(self) -> NoReturn:
        """
        Create an empty file.
        """
        file = open(self.filename, "w+")
        file.close()

    def write(self, string: str, mode="w+") -> NoReturn:
        """
        Write into the file.

        Parameters
        ----------
        string : str
            string to write into the file
        """
        if 'w' not in mode:
            raise ValueError("you must write (w) in the file")
        with open(self.filename, mode) as file:
            file.write(string)

    def append(self, string: str, mode="a+") -> NoReturn:
        """
        Write after the content of the file.

        Parameters
        ----------
        string : str
            string to append to the file
        """
        if 'a' not in mode:
            raise ValueError("you must add (a) in the file")
        with open(self.filename, 'a+') as file:
            file.write(string)

    def read(self, mode="r+") -> str:
        """
        Read all the file.

        Returns
        -------
        string : str
            content of the file
        """
        if 'r' not in mode:
            raise ValueError("you must read (r) from the file")
        with open(self.filename, 'r+') as file:
            data = file.read()
        return data

    def remove(self) -> NoReturn:
        """
        Remove the file.
        """
        os.remove(self.filename)

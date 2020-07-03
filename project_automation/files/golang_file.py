from typing import NoReturn

from project_automation.files import CustomFileExtension


class GolangFile(CustomFileExtension):
    """
    Represents a `.go` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "go"
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
        content = """package main

import (
    "fmt"
)

func main(){
    fmt.Println("Hello World")
}
"""
        self.write(content)

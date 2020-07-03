from typing import NoReturn

from project_automation.files import CustomFileExtension


class PythonFile(CustomFileExtension):
    """
    Represents a `.py` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "py"
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
        content = """def main():
    print("Hello World")

if __name__ == '__main__':
    main()
"""
        self.write(content)

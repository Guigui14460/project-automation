from typing import NoReturn

from project_automation.files import CustomFileExtension
from project_automation.utils import get_gitignore_content


class GitIgnoreFile(CustomFileExtension):
    """
    Represents a `.gitignore` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "gitignore"
    }

    def __init__(self, path: str, languages_used: list) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the file (not add the filename)
        languages_used : list of strings
            list of all used languages in the project
        """
        self.languages_used = languages_used
        super().__init__(path, "")

    def init(self) -> NoReturn:
        """
        Initialize the content of the file.
        """
        self.write(get_gitignore_content(self.languages_used))

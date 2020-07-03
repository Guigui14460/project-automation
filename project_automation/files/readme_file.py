import os
from typing import NoReturn

from .file import File


class ReadMeFile(File):
    """
    Represents a `README.md` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    def __init__(self, path: str) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the file (not add the filename)
        """
        File.__init__(self, os.path.join(path, "README.md"))

    def write_title(self, title: str, title_degree: int = 1) -> NoReturn:
        """
        Write title into the file.

        Parameters
        ----------
        title : str
            title to write into the file
        title_degree : int
            degree of the title
        """
        if not 1 <= title_degree <= 4:
            raise ValueError("title_degree must be between 1 and 4")
        self.append(f"{'#'*title_degree} {title}\n\n")

    def write_paragraph(self, paragraph: str) -> NoReturn:
        """
        Write paragraph into the file after other contents.
        To overwrite the file, use the `write` method.

        Parameters
        ----------
        paragraph : str
            paragraph to append into the file
        """
        self.append(f"{paragraph}\n\n")

    def write_code(self, code: str, language: str = None) -> NoReturn:
        """
        Write code into the file after other contents.
        To overwrite the file, use the `write` method.

        Parameters
        ----------
        code : str
            code to append into the file
        language : str
            programming language for syntax color
        """
        self.append(
            f"```{language if language is not None else ''}\n{code}\n```\n\n")

    def write_from_dict(self, params: dict) -> NoReturn:
        """
        Write some text from a dictionnary into the file after other contents.
        To overwrite the file, use the `write` method.

        Parameters
        ----------
        params : dict
            dictionnary of text to append into the file
        """
        for param in params:
            getattr(self, f"write_{params[param][0]}")(*params[param][1:])

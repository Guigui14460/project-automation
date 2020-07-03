from typing import NoReturn

from project_automation.files import CustomFileExtension
from project_automation.utils import write_in_json_file, read_from_json_file


class JSONFile(CustomFileExtension):
    """
    Represents a `.json` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "json",
        "indentation": 2,
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
        self.write("\"use strict\"\n\nconsole.log('Hello World')")

    def write(self, data: dict) -> NoReturn:
        """
        Write into the file.

        Parameters
        ----------
        data : dict
            all data to put in the file
        """
        self.data = data
        write_in_json_file(self.filename, data, self.CONFIG['indentation'])

    def append(self, data_to_append: dict) -> NoReturn:
        """
        Write after the content of the file.

        Parameters
        ----------
        data_to_append : dict
            data to append at the enf of the file
        """
        self.data.update(data_to_append)
        write_in_json_file(self.filename, self.data,
                           self.CONFIG['indentation'])

    def read(self) -> str:
        """
        Read all the file.

        Returns
        -------
        data : dict
            content of the file
        """
        return read_from_json_file(self.filename)

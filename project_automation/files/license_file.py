from datetime import datetime
import os
from typing import NoReturn

from project_automation.settings import LICENSE_MODE_SHORTCUT
from .file import File


class LicenseFile(File):
    """
    Represents a `LICENSE` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    def __init__(self, path: str, mode: str, username: str) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the file (not add the filename)
        mode : str
            type of the license to use
        username : str
            name of the current user
        """
        File.__init__(self, os.path.join(path, "LICENSE"))
        try:
            license_str = LICENSE_MODE_SHORTCUT[mode.lower()]
            license_str = license_str.replace(
                "year_to_add", str(datetime.today().year))
            license_str = license_str.replace("username_to_add", username)
        except:
            license_str = LICENSE_MODE_SHORTCUT['unlicense']
        self.write(license_str)

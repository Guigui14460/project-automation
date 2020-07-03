import sys
from typing import NoReturn

from .command_not_exists import CommandNotExistsError


class PythonCommandNotExists(CommandNotExistsError):
    """
    Raised when the `python`/`python3` command does not recognized by the system.

    Attributes
    ----------
    message : str
        string to display the error
    cmd_not_reconized : str
        command which are not recognized
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    windows_installation : str 
        windows installation advices
    macos_installation : str
        macOS installation advices
    unix_like_installation : str
        unix-like installation advices
    """

    def __init__(self, allow_install: bool = False) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required packages, False otherwise
        """
        super().__init__('python' if sys.platform == 'win32' else 'python3', allow_install=allow_install, windows_installation="https://www.python.org/downloads/",
                         macos_installation="brew install python3", unix_like_installation="sudo apt install sudo apt-get install -y python3-dev python3-pip")


class PythonPipCommandNotExists(CommandNotExistsError):
    """
    Raised when the `pip`/`pip3` command does not recognized by the system.

    Attributes
    ----------
    message : str
        string to display the error
    cmd_not_reconized : str
        command which are not recognized
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    windows_installation : str 
        windows installation advices
    macos_installation : str
        macOS installation advices
    unix_like_installation : str
        unix-like installation advices
    """

    def __init__(self, allow_install: bool = False) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required packages, False otherwise
        """
        super().__init__('pip' if sys.platform == 'win32' else 'pip3', allow_install=allow_install, windows_installation="https://www.python.org/downloads/",
                         macos_installation="brew install python3", unix_like_installation="sudo apt install sudo apt-get install -y python3-dev python3-pip")

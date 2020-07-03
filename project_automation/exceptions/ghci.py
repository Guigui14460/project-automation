from typing import NoReturn

from .command_not_exists import CommandNotExistsError


class HaskellCommandNotExists(CommandNotExistsError):
    """
    Raised when the `ghci` command does not recognized by the system.

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
        super().__init__('ghci', allow_install=allow_install, windows_installation="Download the installer at this link : https://get.haskellstack.org/stable/windows-x86_64-installer.exe",
                         macos_installation="curl -sSL https://get.haskellstack.org/ | sh OR wget -qO- https://get.haskellstack.org/ | sh", unix_like_installation="sudo apt-get install haskell-platform")

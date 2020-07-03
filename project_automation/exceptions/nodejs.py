from typing import NoReturn

from .command_not_exists import CommandNotExistsError


class NodeJSCommandNotExists(CommandNotExistsError):
    """
    Raised when the NodeJS is not installed in the system.

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

    def __init__(self, cmd_not_reconized: str, allow_install: bool = False) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        cmd_not_reconized : str
            command which are not recognized
        allow_install : bool
            True if you want to automatically install the required packages, False otherwise
        """
        super().__init__(cmd_not_reconized, allow_install=allow_install, windows_installation="https://nodejs.org/en/",
                         macos_installation="brew install node", unix_like_installation="sudo apt install build-essential\nsudo apt-get install nodejs npm")


class NPMCommandNotExists(NodeJSCommandNotExists):
    """
    Raised when the `npm` command does not recognized by the system.

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
        super().__init__('npm', allow_install=allow_install)


class NPXCommandNotExists(NodeJSCommandNotExists):
    """
    Raised when the `npx` command does not recognized by the system.

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
        super().__init__('npx', allow_install=allow_install)
        print("Node version must be >= 8.10 (or npm 5.2+)? More info at this link : https://create-react-app.dev/docs/getting-started/")

from typing import NoReturn

from .command_not_exists import CommandNotExistsError


class FlutterCommandNotExists(CommandNotExistsError):
    """
    Raised when the `flutter` command does not recognized by the system.

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
        super().__init__('flutter', allow_install=allow_install, windows_installation="https://flutter.dev/docs/get-started/install/windows",
                         macos_installation="Follow this instructions : https://flutter.dev/docs/get-started/install/macos", unix_like_installation="Follow this instructions : https://flutter.dev/docs/get-started/install/linux")

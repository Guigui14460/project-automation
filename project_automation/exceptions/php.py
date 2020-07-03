from typing import NoReturn

from .command_not_exists import CommandNotExistsError


class PHPCommandNotExists(CommandNotExistsError):
    """
    Raised when the `php` command does not recognized by the system.

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
        super().__init__('php', allow_install=allow_install, windows_installation="https://windows.php.net/download\nAfter, you need to put the extracted files at the root of your machine and add the path to the environment variables.",
                         macos_installation="curl -s http://php-osx.liip.ch/install.sh | bash -s 7.3\nexport PATH=/usr/local/php5/bin:$PATH", unix_like_installation="sudo apt install php libapache2-mod-php")

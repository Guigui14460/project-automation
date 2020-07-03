import sys
from typing import NoReturn

from project_automation.utils import execute_command, execute_command2


class CommandNotExistsError(Exception):
    """
    Raised when the command does not recognized by the system.

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

    def __init__(self, cmd_not_reconized: str, allow_install: bool = False, windows_installation: str = "", macos_installation: str = "", unix_like_installation: str = "") -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
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
        self.cmd_not_reconized = cmd_not_reconized
        self.allow_install = allow_install
        self.message = ""
        if not allow_install or sys.platform == "win32":
            self.message += f"{cmd_not_reconized} command is not recognized\nExecute the following instruction to install it:"
        self.windows_installation = windows_installation
        self.macos_installation = macos_installation
        self.unix_like_installation = unix_like_installation
        self.modify_message()
        super().__init__(self.message)

    def modify_message(self) -> NoReturn:
        """
        Modify the message in function of the OS.
        """
        self.message += "\n{}"
        if sys.platform == 'win32':
            code, _, _ = execute_command("winget --version")
            winget_to_install = "winget available soon\n"
            self.message = self.message.format(
                f"{winget_to_install if not code else ''}{'Download and install the binary at this URL: ' + self.windows_installation}\nIf it's already installed, add the command to the PATH environment variables")
        else:
            if sys.platform == 'darwin':
                code, _, _ = execute_command("brew --version")
                homebrew_to_install = "Install homebrew here: https://brew.sh/\nor lunch: /usr/bin/ruby -e \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)\"\n"
                self.message = self.message.format(
                    f"{homebrew_to_install if not code and 'brew' in self.macos_installation else ''}{self.macos_installation}")
            else:
                linux_to_install = "sudo apt update\nsudo apt upgrade\n"
                self.message = self.message.format(
                    f"{linux_to_install if 'apt' in self.unix_like_installation else ''}{self.unix_like_installation}")

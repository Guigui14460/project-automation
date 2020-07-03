from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class TypescriptCommand(CommandProgram):
    """
    Command to verify if ``tsc`` command is recognized by the operating system.
    If its not verify, the class install it automatically if you want.
    """

    def __init__(self, allow_install: bool, update_package_manager: bool = True) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required package, False otherwise
        update_package_manager : bool
            allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
        """
        windows = WindowsInstallationPackage(
            choco_command="choco install typescript",
            standard_command="npm install -g typescript",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            standard_command="npm install -g typescript",
            brew_command="brew install typescript",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            standard_command="npm install -g typescript",
            update_package_manager=update_package_manager
        )
        super().__init__("tsc --version", allow_install,
                         windows, macos, linux)

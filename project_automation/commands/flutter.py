from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class FlutterCommand(CommandProgram):
    """
    Command to verify if ``flutter`` command is recognized by the operating system.
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
            windows_download_link="https://flutter.dev/docs/get-started/install/windows",
            scoop_command="scoop install flutter",
            choco_command="choco install flutter",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://flutter.dev/docs/get-started/install/macos",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://flutter.dev/docs/get-started/install/linux",
            update_package_manager=update_package_manager
        )
        super().__init__("flutter --version", allow_install,
                         windows, macos, linux)

from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class DenoCommand(CommandProgram):
    """
    Command to verify if ``deno`` command is recognized by the operating system.
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
            windows_download_link="https://deno.land/",
            standard_command="powershell.exe -command \"iwr https://deno.land/x/install/install.ps1 -useb | iex\"",
            scoop_command="scoop install deno",
            choco_command="choco install deno",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://deno.land/",
            brew_command="brew install unzip deno",
            standard_command="curl -fsSL https://deno.land/x/install/install.sh",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://deno.land/",
            standard_command="curl -fsSL https://deno.land/x/install/install.sh | sh",
            update_package_manager=update_package_manager
        )
        super().__init__("deno --version", allow_install,
                         windows, macos, linux)

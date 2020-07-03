from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class GitCommand(CommandProgram):
    """
    Command to verify if ``git`` command is recognized by the operating system.
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
            windows_download_link="https://git-scm.com/download/win",
            winget_command="winget install Git.Git",
            scoop_command="scoop install git",
            choco_command="choco install git",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://git-scm.com/download/mac",
            brew_command="brew install git",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://git-scm.com/download/linux",
            apt_command="sudo apt-get install git",
            dnf_command="sudo dnf install git",
            yum_command="sudo yum install git",
            pacman_command="sudo pacman -S git",
            update_package_manager=update_package_manager
        )
        super().__init__("git --version", allow_install,
                         windows, macos, linux)

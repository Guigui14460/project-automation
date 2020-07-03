from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class GCCCommand(CommandProgram):
    """
    Command to verify if ``gcc`` command is recognized by the operating system.
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
            windows_download_link="https://osdn.net/projects/mingw/releases/",
            scoop_command="scoop install gcc",
            choco_command="choco install mingw",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://apps.apple.com/us/app/xcode/id497799835?mt=12",
            brew_command="brew install gcc",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            apt_command="sudo apt-get install build-essential",
            dnf_command="sudo dnf install gcc",
            yum_command="sudo yum install gcc",
            pacman_command="sudo pacman -S gcc",
            update_package_manager=update_package_manager
        )
        super().__init__("gcc --version", allow_install,
                         windows, macos, linux)

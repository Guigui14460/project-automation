from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class GHCCommand(CommandProgram):
    """
    Command to verify if ``ghc`` command is recognized by the operating system.
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
            windows_download_link="https://get.haskellstack.org/stable/windows-x86_64-installer.exe",
            winget_command="winget install commercialstack.stack",
            scoop_command="scoop install haskell",
            choco_command="choco install haskell-dev",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://www.haskell.org/platform/#osx",
            standard_command="curl -sSL https://get.haskellstack.org/ | sh",
            brew_command="brew install ghc",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://www.haskell.org/platform/#linux-source",
            standard_command="curl -sSL https://get.haskellstack.org/ | sh",
            apt_command="sudo apt-get install haskell-platform",
            dnf_command="sudo dnf install haskell-platform",
            yum_command="sudo yum install haskell-platform",
            update_package_manager=update_package_manager
        )
        super().__init__("ghc --version", allow_install,
                         windows, macos, linux)

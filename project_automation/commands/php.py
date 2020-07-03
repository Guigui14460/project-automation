from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class PHPCommand(CommandProgram):
    """
    Command to verify if ``php`` command is recognized by the operating system.
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
            windows_download_link="https://windows.php.net/download",
            scoop_command="scoop install php",
            choco_command="choco install php",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://www.php.net/downloads",
            standard_command="curl -s http://php-osx.liip.ch/install.sh | bash -s 7.3",
            brew_command="brew install php",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://www.php.net/downloads",
            apt_command="sudo apt install php libapache2-mod-php",
            dnf_command="sudo dnf install php-cli",
            yum_command="sudo yum install php php-cli",
            pacman_command="sudo pacman -S php",
            update_package_manager=update_package_manager
        )
        super().__init__("php --version", allow_install,
                         windows, macos, linux)

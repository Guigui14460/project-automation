from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class NodeCommand(CommandProgram):
    """
    Command to verify if a NodeJS command is recognized by the operating system.
    If its not verify, the class install it automatically if you want.
    """

    def __init__(self, cmd: str, allow_install: bool, update_package_manager: bool = True) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        cmd : str
            node command to test
        allow_install : bool
            True if you want to automatically install the required package, False otherwise
        update_package_manager : bool
            allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
        """
        windows = WindowsInstallationPackage(
            windows_download_link="https://nodejs.org/en/",
            winget_command="winget install OpenJS.NodeJS",
            scoop_command="scoop install nodejs",
            choco_command="choco install nodejs",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://nodejs.org/en/",
            brew_command="brew install node",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://nodejs.org/en/",
            apt_command="sudo apt-get install nodejs npm",
            dnf_command="sudo dnf install nodejs",
            yum_command="sudo yum install nodejs12",
            pacman_command="sudo pacman -S nodejs npm",
            update_package_manager=update_package_manager
        )
        super().__init__(cmd, allow_install,
                         windows, macos, linux)


class NPMCommand(NodeCommand):
    """
    Command to verify if ``npm`` command is recognized by the operating system.
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
        super().__init__("npm --version")


class NPXCommand(NodeCommand):
    """
    Command to verify if ``npx`` command is recognized by the operating system.
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
        super().__init__("npx --version")

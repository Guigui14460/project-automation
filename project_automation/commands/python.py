import sys
from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class GeneralPythonCommand(CommandProgram):
    """
    Command to verify if a python command is recognized by the operating system.
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
            windows_download_link="https://www.python.org/downloads/",
            winget_command="winget install Python.Python",
            scoop_command="scoop install python",
            choco_command="choco install python pip",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://www.python.org/downloads/",
            brew_command="brew install python3",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            apt_command="sudo apt-get install -y python3-dev python3-pip",
            dnf_command="sudo dnf install python3 python3-virtualenv",
            yum_command="sudo yum install -y python3-devel.x86_64 python-pip",
            pacman_command="sudo pacman -S python3 python-pip python-virtualenv python-pipenv",
            update_package_manager=update_package_manager
        )
        super().__init__(cmd, allow_install,
                         windows, macos, linux)


class PythonCommand(GeneralPythonCommand):
    """
    Command to verify if ``python`` or ``python3`` command is recognized by the operating system.
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
        super().__init__(f"{'python' if sys.platform == 'win32' else 'python3'} --version",
                         allow_install, update_package_manager)


class PythonPipCommand(GeneralPythonCommand):
    """
    Command to verify if ``pip`` or ``pip3`` command is recognized by the operating system.
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
        super().__init__(f"{'pip' if sys.platform == 'win32' else 'pip3'} --version",
                         allow_install, update_package_manager)


class PythonVirtualEnvCommand(GeneralPythonCommand):
    """
    Command to verify if ``python -m venv`` or ``python3 -m venv`` command is recognized by the operating system.
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
            standard_command="python -m pip install virtualenv",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            standard_command="python3 -m pip install virtualenv",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            standard_command="sudo pip3 install virtualenv",
            dnf_command="sudo dnf install python3-virtualenv",
            pacman_command="sudo pacman -S python-virtualenv",
            update_package_manager=update_package_manager
        )
        super().__init__(f"{'python' if sys.platform == 'win32' else 'python3'} -m venv -h",
                         allow_install, windows, macos, linux)


class PythonPipenvCommand(CommandProgram):
    """
    Command to verify if ``pipenv`` command is recognized by the operating system.
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
            standard_command="python -m pip install pipenv",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            standard_command="python3 -m pip install pipenv",
            brew_command="brew install pipenv",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            standard_command="sudo pip3 install pipenv",
            pacman_command="sudo pacman -S python-pipenv",
            update_package_manager=update_package_manager
        )
        super().__init__("pipenv -h",
                         allow_install, windows, macos, linux)

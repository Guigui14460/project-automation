import sys
from typing import NoReturn

from project_automation.settings import SHELL_COLORS
from project_automation.utils import execute_command, execute_command2
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class CommandProgram:
    """
    Command to verify if its recognized by the operating system.
    If its not verify, the class install it automatically if you want.
    """

    def __init__(self,
                 cmd_to_test: str,
                 allow_install: bool,
                 windows_installer: WindowsInstallationPackage,
                 macos_installer: MacOSInstallationPackage,
                 linux_installer: GNULinuxDistributionInstallationPackage) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        cmd_to_test : str
            command to test
        allow_install : bool
            True if you want to automatically install the required package, False otherwise
        windows_installer : project_automation.exceptions.utils.WindowsInstallationPackage
            installer for Windows
        macos_installer : project_automation.exceptions.utils.MacOSInstallationPackage
            installer for MacOS
        linux_installer : project_automation.exceptions.utils.GNULinuxDistributionInstallationPackage
            installer for GNU/Linux
        """
        code, _, _ = execute_command(cmd_to_test)
        if code != 0:
            if sys.platform == 'win32':
                windows_installer.install(allow_install)
            elif sys.platform == 'darwin':
                macos_installer.install(allow_install)
            else:
                linux_installer.install(allow_install)
            if not allow_install:
                print(
                    f"{SHELL_COLORS['red']}Error : You cannot continue without install this package at least !{SHELL_COLORS['endcolor']}")
                sys.exit(1)

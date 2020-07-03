import sys
from typing import NoReturn

from project_automation.settings import SHELL_COLORS
from project_automation.utils import execute_command, execute_command2


class WindowsInstallationPackage:
    """
    Windows package installer shortcut.
    It allows users to install or give information to install packages/programs on the Windows operating system.

    Attributes
    ----------
    windows_download_link : str
        link to download Windows installer of the given package or program
    standard_command : str
        command to install package/program via standard shell
    winget_command : str
        command to install package/program via Winget, https://docs.microsoft.com/en-us/windows/package-manager/winget/
    scoop_command : str
        command to install package/program via scoop, https://scoop.sh/
    choco_command : str
        command to install package/program via choco, https://chocolatey.org/
    update_package_manager : bool
        allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
    """

    def __init__(self,
                 windows_download_link: str = None,
                 standard_command: str = None,
                 winget_command: str = None,
                 scoop_command: str = None,
                 choco_command: str = None,
                 update_package_manager: bool = True) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        windows_download_link : str
            link to download Windows installer of the given package or program
        standard_command : str
            command to install package/program via standard shell
        winget_command : str
            command to install package/program via Winget, https://docs.microsoft.com/en-us/windows/package-manager/winget/
        scoop_command : str
            command to install package/program via scoop, https://scoop.sh/
        choco_command : str
            command to install package/program via choco, https://chocolatey.org/
        update_package_manager : bool
            allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
        """
        self.windows_download_link = windows_download_link
        self.standard_command = standard_command
        self.winget_command = winget_command
        self.scoop_command = scoop_command
        self.choco_command = choco_command
        self.update_package_manager = update_package_manager

    def install(self, allow_install: bool) -> NoReturn:
        """
        Install the needed package/program.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required package, False otherwise
            If the value of this parameter is False, it displays all the possibilities to install the required package
        """
        code_winget, _, _ = execute_command("winget --version")
        code_scoop, _, _ = execute_command("scoop help")
        code_choco, _, _ = execute_command("choco --version")
        if allow_install:
            if self.scoop_command is not None and code_scoop == 0:
                execute_command2("scoop bucket add extras")
                if self.update_package_manager:
                    execute_command2("scoop update")
                    execute_command2("scoop update *")
                execute_command2(self.scoop_command)
            elif self.choco_command is not None and code_choco == 0:
                if self.update_package_manager:
                    execute_command2("choco upgrade chocolatey")
                    execute_command2("choco outdated")
                execute_command2(self.choco_command)
            elif self.winget_command is not None and code_winget == 0:
                execute_command2(self.winget_command)
            elif self.standard_command is not None:
                execute_command2(self.standard_command)
            elif self.windows_download_link is not None:
                print(
                    f"Download the file at this link : {SHELL_COLORS['underline']}{self.windows_download_link}{SHELL_COLORS['endcolor']} and put the path in your {SHELL_COLORS['bold']}PATH{SHELL_COLORS['endcolor']} environment variable")
                sys.exit(1)
            else:
                print(
                    f"{SHELL_COLORS['red']}You cannot install this package or it isn't referenced here ...{SHELL_COLORS['endcolor']}")
                sys.exit(1)
        else:
            if self.standard_command is not None and self.scoop_command is None and self.winget_command is None and self.windows_download_link is None and self.choco_command is None:
                print(
                    f"{SHELL_COLORS['red']}You are no way to install this package ...{SHELL_COLORS['endcolor']}")
            else:
                print("You can install from multiple ways :")
                if self.windows_download_link is not None:
                    print(
                        f"\t- Download the file at this link : {SHELL_COLORS['underline']}{self.windows_download_link}{SHELL_COLORS['endcolor']} and put the path in your {SHELL_COLORS['bold']}PATH{SHELL_COLORS['endcolor']} environment variable")
                if self.standard_command is not None:
                    print(
                        f"\t- Launch the following command : {self.standard_command}")
                if self.winget_command is not None and code_winget == 0:
                    print(
                        f"\t- Launch the following command : {self.winget_command}")
                if self.scoop_command is not None and code_scoop == 0:
                    print(
                        f"\t- Launch the following command : {self.scoop_command}")
                if self.choco_command is not None and code_choco == 0:
                    print(
                        f"\t- Launch the following command : {self.choco_command}")


class MacOSInstallationPackage:
    """
    MacOS package installer shortcut.
    It allows users to install or give information to install packages/programs on the Mac operating system.

    Attributes
    ----------
    macos_download_link : str
        link to download MacOS installer of the given package or program
    standard_command : str
        command to install package/program via standard shell
    brew_command : str
        command to install package/program via Homebrew, https://brew.sh/
    update_package_manager : bool
        allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
    """

    def __init__(self,
                 macos_download_link: str = None,
                 standard_command: str = None,
                 brew_command: str = None,
                 update_package_manager: bool = True) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        macos_download_link : str
            link to download MacOS installer of the given package or program
        standard_command : str
            command to install package/program via standard shell
        brew_command : str
            command to install package/program via Homebrew, https://brew.sh/
        update_package_manager : bool
            allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
        """
        self.macos_download_link = macos_download_link
        self.standard_command = standard_command
        self.brew_command = brew_command
        self.update_package_manager = update_package_manager

    def install(self, allow_install: bool) -> NoReturn:
        """
        Install the needed package/program.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required package, False otherwise
            If the value of this parameter is False, it displays all the possibilities to install the required package
        """
        code_brew, _, _ = execute_command("brew --version")
        if allow_install:
            if self.brew_command is not None:
                if code_brew != 0:
                    execute_command2(
                        "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)\"")
                if self.update_package_manager:
                    execute_command2("brew update")
                    execute_command2("brew upgrade")
                execute_command2(self.brew_command)
            elif self.standard_command is not None:
                execute_command2(self.standard_command)
            elif self.macos_download_link is not None:
                print(
                    f"Download the file at this link : {SHELL_COLORS['underline']}{self.macos_download_link}{SHELL_COLORS['endcolor']} and put the path in your {SHELL_COLORS['bold']}PATH{SHELL_COLORS['endcolor']} environment variable")
                sys.exit(1)
            else:
                print(
                    f"{SHELL_COLORS['red']}You cannot install this package or it isn't referenced here ...{SHELL_COLORS['endcolor']}")
                sys.exit(1)
        else:
            if self.macos_download_link is None and self.brew_command is None and self.standard_command is not None:
                print(
                    f"{SHELL_COLORS['red']}You are no way to install this package ...{SHELL_COLORS['endcolor']}")
            else:
                print("You can install from multiple ways :")
                if self.macos_download_link is not None:
                    print(
                        f"\t- Download the file at this link : {SHELL_COLORS['underline']}{self.macos_download_link}{SHELL_COLORS['endcolor']} and put the path in your {SHELL_COLORS['bold']}PATH{SHELL_COLORS['endcolor']} environment variable")
                if self.standard_command is not None:
                    print(
                        f"\t- Launch the following command : {self.standard_command}")
                if self.brew_command is not None:
                    if code_brew != 0:
                        execute_command2(
                            "/bin/bash -c \"$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)\"")
                    print(
                        f"\t- Launch the following command : {self.brew_command}")


class GNULinuxDistributionInstallationPackage:
    """
    GNU/Linux package installer shortcut.
    It allows users to install or give information to install packages/programs on the GNU/Linux operating system.

    Attributes
    ----------
    linux_download_link : str
        link to download Linux installer of the given package or program
    standard_command : str
        command to install package/program via standard shell
    apt_command : str
        command to install package/program via APT, for Debian-based distrib
    dnf_command : str
        command to install package/program via DNF, for RedHat-based, CentOS-based, and Fedora-based distrib
    yum_command : str
        command to install package/program via YUM, for RedHat-based, CentOS-based, and Fedora-based old distrib
    pacman_command : str
        command to install package/program via Pacman, for ArchLinux-based distrib
    update_package_manager : bool
        allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
    """

    def __init__(self,
                 linux_download_link: str = None,
                 standard_command: str = None,
                 apt_command: str = None,
                 dnf_command: str = None,
                 yum_command: str = None,
                 pacman_command: str = None,
                 update_package_manager: bool = True) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        linux_download_link : str
            link to download Linux installer of the given package or program
        standard_command : str
            command to install package/program via standard shell
        apt_command : str
            command to install package/program via APT, for Debian-based distrib
        dnf_command : str
            command to install package/program via DNF, for RedHat-based, CentOS-based, and Fedora-based distrib
        yum_command : str
            command to install package/program via YUM, for RedHat-based, CentOS-based, and Fedora-based old distrib
        pacman_command : str
            command to install package/program via Pacman, for ArchLinux-based distrib
        update_package_manager : bool
            allows this program to automatically update and upgrade all packages installed in the system (via the package manager used)
        """
        self.linux_download_link = linux_download_link
        self.standard_command = standard_command
        self.apt_command = apt_command
        self.dnf_command = dnf_command
        self.yum_command = yum_command
        self.pacman_command = pacman_command
        self.update_package_manager = update_package_manager

    def install(self, allow_install: bool) -> NoReturn:
        """
        Install the needed package/program.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required package, False otherwise
            If the value of this parameter is False, it displays all the possibilities to install the required package
        """
        code_aptget, _, _ = execute_command("apt-get --help")
        code_dnf, _, _ = execute_command("dnf --help")
        code_yum, _, _ = execute_command("yum help")
        code_pacman, _, _ = execute_command("pacman -S --help")
        if allow_install:
            if self.apt_command is not None and code_aptget == 0:
                if self.update_package_manager:
                    execute_command2("sudo apt-get update")
                    execute_command2("sudo apt-get upgrade")
                execute_command2(self.apt_command)
            elif self.dnf_command is not None and code_dnf == 0:
                if self.update_package_manager:
                    execute_command2("sudo dnf upgrade")
                execute_command2(self.dnf_command)
            elif self.yum_command is not None and code_yum == 0:
                if self.update_package_manager:
                    execute_command2("sudo yum update")
                    execute_command2("sudo yum upgrade")
                execute_command2(self.yum_command)
            elif self.pacman_command is not None and code_pacman == 0:
                if self.update_package_manager:
                    execute_command2("pacman -Syu")
                execute_command2(self.pacman_command)
            elif self.standard_command is not None:
                execute_command2(self.standard_command)
            elif self.linux_download_link is not None:
                print(
                    f"Download the file at this link : {SHELL_COLORS['underline']}{self.linux_download_link}{SHELL_COLORS['endcolor']} and put the path in your {SHELL_COLORS['bold']}PATH{SHELL_COLORS['endcolor']} environment variable")
                sys.exit(1)
            else:
                print(
                    f"{SHELL_COLORS['red']}No command match with your Linux distribution or it isn't referenced here ...{SHELL_COLORS['endcolor']}")
                sys.exit(1)
                print(
                    f"{SHELL_COLORS['warning']}Try to search on Intenet for your distribution ;){SHELL_COLORS['endcolor']}")
                sys.exit(1)
        else:
            if self.standard_command is not None and self.linux_download_link is None and self.apt_command is None and self.dnf_command is None and self.yum_command is None and self.pacman_command is None:
                print(
                    f"{SHELL_COLORS['red']}You are no way to install this package or  ...{SHELL_COLORS['endcolor']}")
            else:
                print("You can install from multiple ways :")
                if self.linux_download_link is not None:
                    print(
                        f"\t- Download the file at this link : {SHELL_COLORS['underline']}{self.linux_download_link}{SHELL_COLORS['endcolor']} and put the path in your {SHELL_COLORS['bold']}PATH{SHELL_COLORS['endcolor']} environment variable")
                if self.standard_command is not None:
                    print(
                        f"\t- Launch the following command : {self.standard_command}")
                if self.apt_command is not None and code_aptget == 0:
                    print(
                        f"\t- Launch the following command : {self.apt_command}")
                elif self.dnf_command is not None and code_dnf == 0:
                    print(
                        f"\t- Launch the following command : {self.dnf_command}")
                elif self.yum_command is not None and code_yum == 0:
                    print(
                        f"\t- Launch the following command : {self.yum_command}")
                elif self.pacman_command is not None and code_pacman == 0:
                    print(
                        f"\t- Launch the following command : {self.pacman_command}")

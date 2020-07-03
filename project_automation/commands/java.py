from typing import NoReturn

from .command_program import CommandProgram
from .utils import WindowsInstallationPackage, MacOSInstallationPackage, GNULinuxDistributionInstallationPackage


class JavaCommand(CommandProgram):
    """
    Command to verify if ``java`` command is recognized by the operating system.
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
            windows_download_link="https://www.java.com/en/download/",
            choco_command="choco install javaruntime",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://www.clubic.com/telecharger-fiche421557-java-runtime-environment.html",
            brew_command="brew install java",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://git-scm.com/download/linux",
            apt_command="sudo apt-get install default-jre",
            dnf_command="sudo dnf install java-latest-openjdk-devel.x86_64",
            yum_command="sudo yum install java-11-openjdk-devel",
            pacman_command="sudo pacman -S java",
            update_package_manager=update_package_manager
        )
        super().__init__("java --version", allow_install,
                         windows, macos, linux)


class JavacCommand(CommandProgram):
    """
    Command to verify if ``javac`` command is recognized by the operating system.
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
            windows_download_link="https://www.oracle.com/java/technologies/javase-downloads.html",
            choco_command="choco install openjdk.portable",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://www.oracle.com/java/technologies/javase-downloads.html",
            brew_command="brew install openjdk",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://www.oracle.com/java/technologies/javase-downloads.html",
            apt_command="sudo apt-get install default-jdk",
            dnf_command="sudo dnf install java-latest-openjdk-devel.x86_64",
            yum_command="sudo yum install java-1.8.0-openjdk-devel",
            pacman_command="sudo pacman -S jdk-openjdk",
            update_package_manager=update_package_manager
        )
        super().__init__("javac --version", allow_install,
                         windows, macos, linux)


class MavenCommand(CommandProgram):
    """
    Command to verify if ``mvn`` command is recognized by the operating system.
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
            windows_download_link="https://maven.apache.org/download.cgi",
            scoop_command="scoop install maven",
            choco_command="choco install maven",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://maven.apache.org/download.cgi",
            brew_command="brew install maven",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://maven.apache.org/download.cgi",
            apt_command="sudo apt-get install maven",
            dnf_command="sudo dnf install maven",
            yum_command="sudo yum install maven",
            pacman_command="sudo pacman -S maven",
            update_package_manager=update_package_manager
        )
        super().__init__("mvn --version", allow_install,
                         windows, macos, linux)


class AntCommand(CommandProgram):
    """
    Command to verify if ``ant`` command is recognized by the operating system.
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
            windows_download_link="https://ant.apache.org/bindownload.cgi",
            scoop_command="scoop install ant",
            choco_command="choco install ant",
            update_package_manager=update_package_manager
        )
        macos = MacOSInstallationPackage(
            macos_download_link="https://ant.apache.org/bindownload.cgi",
            brew_command="brew install ant",
            update_package_manager=update_package_manager
        )
        linux = GNULinuxDistributionInstallationPackage(
            linux_download_link="https://ant.apache.org/bindownload.cgi",
            apt_command="sudo apt-get install ant",
            update_package_manager=update_package_manager
        )
        super().__init__("ant --version", allow_install,
                         windows, macos, linux)

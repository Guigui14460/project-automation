from typing import NoReturn

from .command_not_exists import CommandNotExistsError


class JavaCommandNotExists(CommandNotExistsError):
    """
    Raised when the `java`, `javadoc` or `jar` commands are not recognized by the system.

    Attributes
    ----------
    message : str
        string to display the error
    cmd_not_reconized : str
        command which are not recognized
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    windows_installation : str 
        windows installation advices
    macos_installation : str
        macOS installation advices
    unix_like_installation : str
        unix-like installation advices
    """

    def __init__(self, cmd_not_reconized: str, allow_install: bool = False) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        cmd_not_reconized : str
            command which are not recognized
        allow_install : bool
            True if you want to automatically install the required packages, False otherwise
        """
        super().__init__(cmd_not_reconized, allow_install=allow_install, windows_installation="https://www.oracle.com/java/technologies/javase-downloads.html",
                         macos_installation="Download and install JDK at this link  : https://www.oracle.com/java/technologies/javase-downloads.html\nor via homebrew : brew cask install java", unix_like_installation="sudo apt install default-jre\nsudo apt install default-jdk")
        print("Warning ! JRE (Java Runtime Environment) and JDK (Java Development Kit) must both be install")


class MavenCommandNotExists(CommandNotExistsError):
    """
    Raised when the `mvn` command is not recognized by the system.

    Attributes
    ----------
    message : str
        string to display the error
    cmd_not_reconized : str
        command which are not recognized
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    windows_installation : str 
        windows installation advices
    macos_installation : str
        macOS installation advices
    unix_like_installation : str
        unix-like installation advices
    """

    def __init__(self, allow_install: bool = False) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required packages, False otherwise
        """
        super().__init__('mvn', allow_install=allow_install, windows_installation="https://maven.apache.org/download.cgi (install the binary archive)",
                         macos_installation="brew install maven", unix_like_installation="sudo apt install maven")


class AntCommandNotExists(CommandNotExistsError):
    """
    Raised when the `ant` command is not recognized by the system.

    Attributes
    ----------
    message : str
        string to display the error
    cmd_not_reconized : str
        command which are not recognized
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    windows_installation : str 
        windows installation advices
    macos_installation : str
        macOS installation advices
    unix_like_installation : str
        unix-like installation advices
    """

    def __init__(self, allow_install: bool = False) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        allow_install : bool
            True if you want to automatically install the required packages, False otherwise
        """
        super().__init__('ant', allow_install=allow_install, windows_installation="https://ant.apache.org/bindownload.cgi (install the binary archive)",
                         macos_installation="brew install ant", unix_like_installation="sudo apt-get install ant")

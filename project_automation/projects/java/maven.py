import os
from typing import Any, NoReturn

from project_automation.commands import MavenCommand
from project_automation.projects.java.java import JavaProject
from project_automation.utils import execute_command, execute_command2


class MavenProject(JavaProject):
    """
    Represents the base of a Java project with Maven to create.

    Attributes
    ----------
    path : str
        path of the parent root of the project
    name : str
        name of the project (used for make directory and github repo)
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    package_name : str
        name of the app to put at the head of the Java files
    company_name : str
        name of the company (for the name of the package and maven)
    github_settings : dict
        some github informations
    installation_verified : bool
        returns if the installation are already been verified
    errors : list of string
        all occured error during project creation (not exceptions)
    user : ~github.AuthenticatedUser or ~github.NamedUser
        github user if ``github_settings`` is not empty
    root : ~files.Folder
        root folder of the project
    """

    CONFIG = {
        'languages': ["Java", "Maven", "XML"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ("paragraph", "Use the Maven integrated tool in Eclipse or Intellij or you can download the Maven Extension for VSCode."),
        },
    }

    def __init__(self, path: str, name: str, package_name: str, company_name: str, executing_scripts: bool = False, github_settings: dict = {}, **kwargs: Any) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the parent root of the project
        name : str
            name of the project (used for make directory and github repo)
        package_name : str
            name of the package to put at the head of the Java files
        company_name : str
            name of the company (for the name of the package and maven)
        executing_scripts : bool
            allows us to create scripts to simplify the usage
        github_settings : dict
            some github informations
        """
        super().__init__(path, package_name, package_name, company_name,
                         executing_scripts=False, generate_files=False, github_settings=github_settings, **kwargs)
        self.installation_verified = False

    def create(self) -> NoReturn:
        """
        Create the structure of the project.

        Seea also
        ---------
        utils.execute_command2
        """
        self.verify_installation()
        os.chdir(os.path.join(self.path, '..'))
        execute_command2(
            f"mvn archetype:generate -DgroupId={self.company_name.lower()}.{self.package_name} -DartifactId={self.package_name} -DarchetypeArtifactId=maven-archetype-quickstart -DinteractiveMode=false")
        super().create()

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        if not self.installation_verified:
            self.installation_verified = True
            super().verify_installation()
            MavenCommand(self.allow_install)

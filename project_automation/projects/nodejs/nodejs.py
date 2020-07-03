import os
from typing import Any, NoReturn

from project_automation.exceptions import NPMCommandNotExists
from project_automation.projects import Project
from project_automation.utils import execute_command


class NodeJSProject(Project):
    """
    Represents the base of NodeJS project to create.

    Attributes
    ----------
    path : str
        path of the parent root of the project
    name : str
        name of the project (used for make directory and github repo)
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    github_settings : dict
        some github informations
    errors : list of string
        all occured error during project creation (not exceptions)
    user : ~github.AuthenticatedUser or ~github.NamedUser
        github user if ``github_settings`` is not empty
    root : ~files.Folder
        root folder of the project
    npm_version : tuple of strings
        npm version
    """

    CONFIG = {
        'languages': ["Javascript", "Node"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ('code', '$ ghci main.hs', 'shell'),
        }
    }

    def __init__(self, path: str, name: str, github_settings: dict = {}, **kwargs: Any) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the parent root of the project
        name : str
            name of the project (used for make directory and github repo)
        github_settings : dict
            some github informations
        **kwargs : Any
            other keywords parameters
        """
        super().__init__(path, name, github_settings=github_settings, **kwargs)

    def create(self) -> NoReturn:
        """
        Create the structure of the project.

        See also
        --------
        utils.execute_command
        """
        super().create()
        os.chdir(self.path)
        execute_command("npm init -y")
        print(
            "To install packages, launch `npm install -D <package_name1> [<package_name2>, ...]`")

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        super().verify_installation()
        code, outs, _ = execute_command(
            f"npm --version")
        if code:
            raise NPMCommandNotExists(allow_install=self.allow_install)
        self.npm_version = tuple(outs[0].split('\n')[0].split('.'))

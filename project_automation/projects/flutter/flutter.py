import os
from typing import Any, NoReturn

from project_automation.commands import FlutterCommand
from project_automation.projects import Project
from project_automation.utils import execute_command2


class FlutterProject(Project):
    """
    Represents the base of a Flutter project to create.

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
    """

    CONFIG = {
        'languages': ["Flutter", "Dart"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ("code", "$ flutter run", "shell")
        },
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
        utils.execute_command2
        """
        super().create()
        os.chdir(os.path.join(self.path, '..'))
        execute_command2(f"flutter create {self.name}")

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        commands.FlutterCommand
        """
        super().verify_installation()
        FlutterCommand(self.allow_install)

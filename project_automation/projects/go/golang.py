from typing import Any, NoReturn

from project_automation.commands import GoCommand
from project_automation.files import GolangFile
from project_automation.projects import Project


class GolangProject(Project):
    """
    Represents the base of Golang project to create.

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
        'languages': ["Go"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Simple run](#simple-run)\n2. [Execute binary program](#execute-binary-program)"),
            '3': ('title', "Simple run", 2),
            '4': ('code', '$ go run main.go', 'shell'),
            '5': ('title', "Execute binary program", 2),
            '6': ('code', '$ go build main.go && main', 'shell'),
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
        """
        super().create()
        self.root.add(GolangFile(self.path, 'main'))

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        commands.GoCommand
        """
        super().verify_installation()
        GoCommand(self.allow_install)

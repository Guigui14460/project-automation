from typing import Any, NoReturn

from project_automation.commands import GPPCommand
from project_automation.files import CPPFile, CHeaderFile
from project_automation.projects import Project


class CPPProject(Project):
    """
    Represents the base of a C++ project to create.

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
        'languages': ["C++"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ("code", "$ g++ main.c add.c -o prog", "shell")
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
        """
        super().create()
        cpp_header_add_file = CHeaderFile(self.path, "add")
        cpp_add_file = CPPFile(self.path, "add")
        cpp_main_file = CPPFile(self.path, "main")
        cpp_main_file.init_main(cpp_add_file)
        self.root.add(cpp_header_add_file, cpp_add_file, cpp_main_file)

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        commands.GPPCommand
        """
        super().verify_installation()
        GPPCommand(self.allow_install)

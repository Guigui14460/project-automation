import os
from typing import Any, NoReturn

from project_automation.commands import NPMCommand, NPXCommand
from project_automation.projects.nodejs.nodejs import NodeJSProject
from project_automation.utils import execute_command, execute_command2


class ReactJSProject(NodeJSProject):
    """
    Represents the base of ReactJS project to create.

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
    use_npx : bool
        use the ``npx`` command
    """

    CONFIG = {
        'languages': ["ReactJS", "Javascript", "Node"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ('code', '$ npm start', 'shell'),
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
        super().__init__(path, name,
                         github_settings=github_settings, **kwargs)

    def create(self) -> NoReturn:
        """
        Create the structure of the project.

        See also
        --------
        utils.execute_command2
        """
        super().create()
        os.chdir(os.path.join(self.path, '..'))
        if self.use_npx:
            if self.allow_install:
                execute_command2(
                    f"npx create-react-app {os.path.basename(self.path)}")
            else:
                print(
                    f"Launch `npx create-react-app {os.path.basename(self.path)}` command to create a ReactJS App")
        else:
            if self.allow_install:
                execute_command2(
                    f"npm init react-app {os.path.basename(self.path)}")
            else:
                print(
                    f"Launch `npm init react-app {os.path.basename(self.path)}` command to create a ReactJS App")

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
        NPMCommand(self.allow_install)
        if self.npm_version >= ('5', '2'):
            NPXCommand(self.allow_install)
            self.use_npx = True
        else:
            self.use_npx = False

from pathlib import Path
import os
from typing import Any, NoReturn, Union

import github

from project_automation.exceptions import GitCommandNotExists
from project_automation.files import (
    File, Folder, GitIgnoreFile, ReadMeFile, LicenseFile,
)
from project_automation.settings import GITHUB_USER, GITHUB_PASS, GITHUB_OAUTH_ACCESS_TOKEN, SHELL_COLORS
from project_automation.utils import execute_command, execute_command2, tree


class Project:
    """
    Represents a simple project to create.

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
        'languages': [],
        'readme_content': {}
    }

    def __init__(self, path: str, name: str, allow_install: bool = False, github_settings: dict = {}, **kwargs: Any) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the parent root of the project
        name : str
            name of the project (used for make directory and github repo)
        allow_install : bool
            True if you want to automatically install the required packages, False otherwise
        github_settings : dict
            some github informations
        **kwargs : Any
            other keywords parameters
        """
        self.errors = []
        try:
            client = None
            if GITHUB_OAUTH_ACCESS_TOKEN is None:
                client = github.Github(GITHUB_USER, GITHUB_PASS)
            else:
                client = github.Github(GITHUB_OAUTH_ACCESS_TOKEN)
            self.user = client.get_user()
        except github.BadCredentialsException:
            self.errors.append("Your Github credentials are bad.")
            self.user = None
        except github.TwoFactorException:
            self.errors.append(
                "You have activate the 2-Factor-Authentication on Github. Use the OAuth access token to bypass the 2FA (developer tab).")
            self.user = None
        self.path = os.path.join(path, name)
        self.name = name
        self.github_settings = github_settings
        self.allow_install = allow_install

    def create(self) -> NoReturn:
        """
        Create the structure of the project.
        """
        self.verify_installation()
        self.root = Folder(self.path)
        readme = ReadMeFile(self.path)
        readme.write_title(self.name)
        readme.write_paragraph(
            "Project generated with `project_automation` module")
        readme.write_from_dict(self.CONFIG['readme_content'])
        gitignore = GitIgnoreFile(self.path, self.CONFIG['languages'])
        self.root.add(readme, gitignore)
        if self.github_settings != {}:
            if self.user is None:
                raise PermissionError(
                    "you must put your credentials into .env file to create repository")
            self.user.create_repo(
                self.name, private=not self.github_settings['public'])
            license_file = LicenseFile(
                self.path, self.github_settings['license'], self.user.name)
            self.root.add(license_file)

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        if self.github_settings != {} and self.user is not None:
            code, _, _ = execute_command("git --version")
            if code:
                raise GitCommandNotExists(allow_install=self.allow_install)

    def commit(self, message="Initial commit") -> NoReturn:
        """
        Commit all the project to the Github repo (if ``github_settings`` attribute is not empty)
        and show all the errors occured in the execution.

        Parameters
        ----------
        message : str
            commit message into the repo

        See also
        --------
        utils.execute_command
        """
        os.chdir(self.path)
        execute_command2(f"cd {self.path}")
        if self.github_settings != {} and self.user is not None:
            execute_command2("git init")
            execute_command2(f"git add {self.path}")
            execute_command2(f"git commit -m \"{message}\"")
            execute_command2(
                f"git remote add origin https://github.com/{self.user.login}/{self.name}.git")
            execute_command2("git push -u origin master")
        elif self.user is None:
            self.errors.append(
                "You cannot push your modification on your repo.")

        error_len = len(self.errors)
        print(
            f"There are {SHELL_COLORS['green'] if error_len == 0 else SHELL_COLORS['red']}{error_len}{SHELL_COLORS['endcolor']} errors arrived during the execution (not exceptions){'' if error_len == 0 else ' :'}")
        for error in self.errors:
            print(f"- {error}")
        self.errors = []

    def structure(self) -> NoReturn:
        """
        Show the structure of the project.

        See also
        --------
        utils.tree
        """
        tree(self.path)

    def remove_project(self) -> NoReturn:
        """
        Remove the whole project.
        """
        self.root.remove_folder()

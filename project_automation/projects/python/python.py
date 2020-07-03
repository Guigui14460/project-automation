import os
import sys
from typing import Any, NoReturn

from project_automation.exceptions import PythonCommandNotExists, PythonPipCommandNotExists
from project_automation.files import Folder, PythonFile
from project_automation.projects import Project
from project_automation.utils import execute_command, execute_command2


class PythonProject(Project):
    """
    Represents the base of a python project to create.

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
    use_env : bool
            True to use a virtual environment, False otherwise
    env_type : str
        type of virtual environment to use.
        You can use 'pipenv' or 'venv' only
    """

    CONFIG = {
        'languages': ["Python"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ("code", "$ python3 main.py", "shell")
        },
        "packages": [],
    }

    def __init__(self, path: str, name: str, use_env: bool = True, env_type: str = "pipenv", github_settings: dict = {}, **kwargs: Any) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the parent root of the project
        name : str
            name of the project (used for make directory and github repo)
        use_env : bool
            True to use a virtual environment, False otherwise
        env_type : str
            type of virtual environment to use.
            You can use 'pipenv' or 'venv' only
        github_settings : dict
            some github informations
        """
        super().__init__(path, name, github_settings=github_settings, **kwargs)
        if 'additionnal_packages' in kwargs.keys() and kwargs['additionnal_packages'] is not None:
            self.CONFIG['packages'].extend(kwargs['additionnal_packages'])
        self.use_env = use_env
        self.env_type = env_type

    def create(self) -> NoReturn:
        """
        Create the structure of the project.
        """
        super().create()
        self.setup_environment()
        py_file = PythonFile(self.path, "main")
        test_dir = Folder(os.path.join(self.path, 'tests'))
        py_test_file = PythonFile(os.path.join(
            self.path, 'tests'), 'test_main')
        py_test_file.write(
            "import unittest\n\nfrom main import main\n\n\nclass MainTest(unittest.TestCase):\n    def test_main(self):\n        self.assertIsNone(main())\n\nif __name__ == '__main__':\n    unittest.main()")
        test_dir.add(py_test_file)
        self.root.add(py_file, test_dir)

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        super().verify_installation()
        python_version_for_system = '3' if sys.platform != 'win32' else ''
        code, _, _ = execute_command(
            f"python{python_version_for_system} --version")
        if code:
            raise PythonCommandNotExists(allow_install=self.allow_install)
        code, _, _ = execute_command(
            f"pip{python_version_for_system} --version")
        if code:
            raise PythonPipCommandNotExists(allow_install=self.allow_install)

        # Env programs
        if self.use_env:
            if self.env_type == "pipenv":
                code, _, _ = execute_command(
                    f"pipenv --version")
                if code:
                    if self.allow_install:
                        execute_command2(
                            f"pip{python_version_for_system} install --user pipenv")

    def setup_environment(self) -> NoReturn:
        """
        Set up the chosen virtual environment.
        Install packages if the user want.
        """
        python_version_for_system = '3' if sys.platform != 'win32' else ''
        if self.use_env:
            if self.env_type == 'pipenv':
                os.chdir(self.path)
                if self.allow_install:
                    execute_command2(
                        f"pipenv install {' '.join(self.CONFIG['packages'])}")
            elif self.env_type == 'venv':
                execute_command2(
                    f"python{python_version_for_system} -m venv {os.path.join(self.path, 'env')}")
                if self.allow_install:
                    if sys.platform == 'win32':
                        execute_command2("env\Scripts\\activate.bat")
                    else:
                        execute_command2(". env/bin/activate")
                    if len(self.CONFIG['packages']) > 0:
                        execute_command2(
                            f"pip install {' '.join(self.CONFIG['packages'])}")
        else:
            if len(self.CONFIG['packages']) > 0 and self.allow_install:
                execute_command2(
                    f"pip{python_version_for_system} install {' '.join(self.CONFIG['packages'])}")

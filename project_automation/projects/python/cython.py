import os
import sys
from typing import Any, NoReturn

from project_automation.commands import GCCCommand
from project_automation.files import Folder, PythonFile, CythonFile, CythonHeaderFile
from project_automation.utils import execute_command
from .python import PythonProject


class CythonProject(PythonProject):
    """
    Represents the base of a cython project to create.

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

    CONFIG_CYTHON = {
        'languages': ["Python", "Cython"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ("code", "$ python3 setup.py build_ext --inplace", "shell"),
            '5': ("code", "$ python3 main.py", 'shell'),
        },
        'packages': ['Cython'],
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
        **kwargs : Any
            other keywords parameters
        """
        self.CONFIG.update(self.CONFIG_CYTHON)
        super().__init__(path, name, use_env=use_env,
                         env_type=env_type, github_settings=github_settings, **kwargs)

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        GCCCommand(self.allow_install)
        super().verify_installation()

    def create(self) -> NoReturn:
        """
        Create the structure of the project.
        """
        super().create()
        py_script_file = CythonFile(self.path, "script")
        py_script_header_file = CythonHeaderFile(self.path, "script")
        py_setup_file = PythonFile(self.path, "setup")
        setup_content = "from distutils.core import setup\nfrom distutils.extension import Extension\nfrom os.path import join, dirname\n\nfrom Cython.Build import cythonize\nfrom Cython.Distutils import build_ext\n\n\n"
        setup_content += "path = dirname(__file__)\n\nextensions = [\n    Extension('script', sources=[join(path, 'script.pyx')]),\n]\n\n"
        setup_content += "setup(\n    cmdclass={'build_ext': build_ext},\n    ext_modules=cythonize(extensions))"
        py_setup_file.write(setup_content)
        self.root.add(py_script_file, py_script_header_file, py_setup_file)

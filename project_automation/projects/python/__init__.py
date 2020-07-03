import argparse
from typing import NoReturn

from project_automation.utils import Parser
from .python import PythonProject
from .cython import CythonProject


__all__ = [
    'PythonProject',
    'CythonProject',
]


class ParserPython(Parser):
    """
    Parser class to add subcommand for Python projects.

    Attributes
    ----------
    subcommand : str
        subcommand to show in the CLI
    parser : argparse.ArgumentParser
        subcommand parser

    See also
    --------
    utils.get_parser_class
    """

    def __init__(self, subparser: argparse._SubParsersAction) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        subparser : argparse._SubParsersAction
            subparser instance to add subcommands
        """
        super().__init__(subparser, 'python',
                         'sub-command to generate Python type project')
        self.parser.add_argument('-t', '--type', choices=[
            'classic', 'cython'], default='classic', help='create some specific python project (classic by default)')
        self.parser.add_argument('--no-env', action='store_true',
                                 default=False, help='no use the python virtual environment (False by default)')
        self.parser.add_argument(
            '--env', choices=['pipenv', 'venv'], help='choice a python virtual environment (pipenv by default)', default='pipenv')
        self.parser.add_argument(
            '-p', '--packages', nargs='+', help='package to install for this specific project')

    def modify_project_settings(self, result: argparse.Namespace, project_settings: dict) -> dict:
        """
        Return the modified project settings if match with subcommand.

        Parameters
        ----------
        result : ~argparse.Namespace
            object returns when called ``parser.parse_args()``
        project_settings : dict
            dictionnary contains all the project settings to generate the correct project

        Returns
        -------
        project_settings : dict
            modified project_settings if needed
        """
        project_settings['use_env'] = not result.no_env
        project_settings['env_type'] = result.env
        project_settings['additionnal_packages'] = result.packages
        if result.type == 'classic':
            project_settings['klass'] = PythonProject
        elif result.type == 'cython':
            project_settings['klass'] = CythonProject
        return project_settings

import argparse
import re
from typing import NoReturn

from project_automation.utils import Parser
from .ant import AntProject
from .java import JavaProject
from .maven import MavenProject


__all__ = [
    'AntProject',
    'JavaProject',
    'MavenProject',
]


class ParserJava(Parser):
    """
    Parser class to add subcommand for Java projects.

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
        super().__init__(subparser, 'java',
                         'sub-command to generate Java type project')
        self.parser.add_argument(
            'package_name', help='name of the main java package')
        self.parser.add_argument('-t', '--type', choices=[
            'classic', 'ant', 'mvn'], default='classic', help='create some specific java project (classic by default)')
        self.parser.add_argument('-c', '--company-name', default='nobody',
                                 help='name of the compagny for the name of the package (nobody by default)')
        self.parser.add_argument('-s', '--scripts', default=False, action='store_true',
                                 help='generate some scripts to simplify usage for "classic" and "ant" only (False by default)')

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
        project_settings['package_name'] = '_'.join(
            re.split(r'[-,:; =+]\s*', result.package_name.lower()))
        project_settings['company_name'] = result.company_name
        project_settings['executing_scripts'] = result.scripts
        if result.type == 'classic':
            project_settings['klass'] = JavaProject
        elif result.type == 'ant':
            project_settings['klass'] = AntProject
        elif result.type == 'mvn':
            project_settings['klass'] = MavenProject
        return project_settings

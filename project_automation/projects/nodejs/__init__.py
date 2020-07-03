import argparse
from typing import NoReturn

from project_automation.utils import Parser
from .nodejs import NodeJSProject
from .reactjs import ReactJSProject
from .webpackjs import WebpackJSProject


__all__ = [
    'NodeJSProject',
    'ReactJSProject',
    'WebpackJSProject',
]


class ParserNodeJS(Parser):
    """
    Parser class to add subcommand for NodeJS projects.

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
        super().__init__(subparser, 'nodejs',
                         'sub-command to generate NodeJS type project')
        self.parser.add_argument('-t', '--type', choices=[
            'classic', 'react', 'webpack'], default='classic', help='create some specific NodeJS project (classic by default with no dependencies)')

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
        if result.type == 'classic':
            project_settings['klass'] = NodeJSProject
        elif result.type == 'react':
            project_settings['klass'] = ReactJSProject
        elif result.type == 'webpack':
            project_settings['klass'] = WebpackJSProject
        return project_settings

import argparse
from typing import NoReturn

from project_automation.utils import Parser
from .simple import SimpleWebsiteProject
from .typescript import TypescriptWebsiteProject


__all__ = [
    'SimpleWebsiteProject',
    'TypescriptWebsiteProject',
]


class ParserWebsite(Parser):
    """
    Parser class to add subcommand for website projects.

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
        super().__init__(subparser, 'website',
                         'sub-command to generate website type project')
        self.parser.add_argument('-t', '--type', choices=[
            'classic', 'typescript'], default='classic', help='create some specific website project (classic by default)')

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
            project_settings['klass'] = SimpleWebsiteProject
        elif result.type == 'typescript':
            project_settings['klass'] = TypescriptWebsiteProject
        return project_settings

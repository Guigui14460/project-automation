import argparse
from typing import NoReturn

from project_automation.utils import Parser
from .deno import DenoProject


__all__ = [
    'DenoProject',
]


class ParserDeno(Parser):
    """
    Parser class to add subcommand for Deno projects.

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
        super().__init__(subparser, 'deno',
                         'sub-command to generate Deno type project')

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
        project_settings['klass'] = DenoProject
        return project_settings

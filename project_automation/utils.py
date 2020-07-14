import abc
import argparse
from itertools import islice, takewhile
import json
import os
from pathlib import Path
import requests
import subprocess
import sys
from typing import ClassVar, NoReturn, Union


SPACE = '    '
BRANCH = '│   '
TEE = '├── '
LAST = '└── '


def tree(dir_path: Union[str, Path], level: int = -1, limit_to_directories: bool = False,
         length_limit: int = 1000) -> NoReturn:
    """
    Visualization of file structure from a given path.

    Parameters
    ----------
    dir_path : str or ~pathlib.Path
        path of the directory to show the tree
    level : int
        level to show the tree depth
    limit_to_directories : bool
        just show directories
    length_limit : int
        limit of directories/files to show
    """
    dir_path = Path(dir_path)
    files = 0
    directories = 0

    def inner(dir_path: Path, prefix: str = '', level: int = -1):
        nonlocal files, directories
        if not level:
            return
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else:
            contents = list(dir_path.iterdir())
        pointers = [TEE] * (len(contents) - 1) + [LAST]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name + "/"
                directories += 1
                extension = BRANCH if pointer == TEE else SPACE
                yield from inner(path, prefix=prefix+extension, level=level-1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1
    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(f'\n{directories} directories' +
          (f', {files} files' if files else ''))


def execute_command(cmd: str, input: list = None, timeout: list = None):
    """
    Execute a simple command.

    Parameters
    ----------
    cmd : str
        command to execute in the terminal
    input : list of string
        list of inputs data to communicate to the process
    timeout : list of integer
        list of timeout to wait if the command returns

    Returns
    -------
    code : int
        the returned code of the executed command
    outs : list of string
        list of the outputs
    errs : list of string
        list of the errors
    """
    if input == None:
        if not timeout == None:
            raise ValueError(
                "input and timeout must be None or list of element")
        input = [None]
        timeout = [None]
    else:
        if timeout == None:
            raise ValueError(
                "input and timeout must be None or list of element")
        if len(input) != len(timeout):
            raise ValueError(
                "input and timeout must have the exact same length")

    input_length = len(input)
    outs, errs = [""]*input_length, [""]*input_length
    print(f"Executing `{cmd}` command ...")
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in range(input_length):
        c = process.communicate(input=input[i], timeout=timeout[i])
        outs[i] = c[0].decode('latin-1')
        errs[i] = c[1].decode('latin-1')
    code = process.returncode
    return code, outs, errs


def execute_command2(cmd: str):
    """
    Execute a simple command and make it interactivable.

    Parameters
    ----------
    cmd : str
        command to execute in the terminal

    Returns
    -------
    code : int
        the returned code of the executed command
    """
    print(f"Executing `{cmd}` command ...")
    return os.system(cmd)


def get_gitignore_content(languages: list) -> str:
    """
    Get the .gitignore files associated to the languages and add them.

    Parameters
    ----------
    languages : list of strings
        the used languages

    Returns
    -------
    all_gitignore : str
        all content of the associated files
    """
    all_gitignore = ""
    for language in languages:
        response = requests.get(
            f"https://raw.githubusercontent.com/github/gitignore/master/{language}.gitignore")
        if response.status_code == 200:
            all_gitignore += response.content.decode("utf-8")
    return all_gitignore


def create_css_rule(selectors: list, properties: dict) -> str:
    """
    Return CSS rule properly formated.

    Paramters
    ---------
    selectors : list of string
        list of the CSS selector to apply all the properties
    properties : dict
        dictionnary of CSS properties to apply

    Returns
    -------
    string : str
        pretty-printed CSS rule
    """
    string_to_add = ", ".join(selectors) + " {"
    for propertyy in properties:
        string_to_add += f"\n    {propertyy}: {properties[propertyy]};"
    string_to_add += "\n}\n\n"
    return string_to_add


def allnamesequal(name: list) -> bool:
    """
    Verify all names are equal.

    Parameters
    ----------
    name : list of strings
        all the names

    Returns
    -------
    all : bool
        True if all the names are equal, False otherwise
    """
    return all(n == name[0] for n in name[1:])


def common_prefix(paths: list) -> str:
    """
    Obtain the common prefix of a list of paths.

    Parameters
    ----------
    paths : list of string
        list of paths

    Returns
    -------
    prefix : str
        the commom path from all paths

    See also
    --------
    allnamesequal
    """
    if len(paths) == 1:
        return paths[0]
    if sys.platform == "win32":
        sep = "\\"
    else:
        sep = "/"
    bydirectorylevels = zip(*[p.split(sep) for p in paths])
    return sep.join(x[0] for x in takewhile(allnamesequal, bydirectorylevels))


def write_in_json_file(filename: str, data: dict, indent_json: int = None) -> int:
    """
    Write the data in a json file.

    Parameters
    ----------
    filename : str
        name of the file
    data : dict
        all data to put in the file
    indent_json : int
        number of spaces the indent the data properly

    Returns
    -------
    file_size : int
        size of the file just written
    """
    file = open(filename, 'w+')
    size = file.write(json.dumps(data, indent=indent_json))
    file.close()
    return size


def read_from_json_file(filename: str) -> dict:
    """
    Read the data from a json file.

    Parameters
    ----------
    filename : str
        name of the file

    Returns
    -------
    data : dict
        all data of the file
    """
    file = open(filename, 'r')
    data = json.loads(file.read())
    file.close()
    return data


class Parser(abc.ABC):
    """
    Parser class allows to add a subparser in the module.

    Attributes
    ----------
    subcommand : str
        subcommand to show in the CLI
    parser : argparse.ArgumentParser
        subcommand parser

    Notes
    -----
    If you don't inherite this class, your children classes or not available in the main program.
    In other words, if you don't use this class, your subcommands are not detected.

    See also
    --------
    get_parser_class
    """

    def __init__(self, subparser: argparse._SubParsersAction, subcommand: str, subcommand_description: str = "") -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        subparser : argparse._SubParsersAction
            subparser instance to add subcommands
        subcommand : str
            name of the subcommand
        subcommand_description : str
            description of the subcommand
        """
        self.subcommand = subcommand
        self.parser = subparser.add_parser(
            subcommand, description=subcommand_description)
        self.parser.add_argument(
            'path', help='path of the parent root for create the project structure')
        self.parser.add_argument(
            'project_name', help='name of the project')

    def get_result(self, result: argparse.Namespace, project_settings: dict) -> dict:
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
        if result.command == self.subcommand:
            project_settings = self.modify_project_settings(
                result, project_settings)
        return project_settings

    @abc.abstractmethod
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
        pass


def get_parent_types(klass: ClassVar) -> list:
    """
    Get recursively all parent types.

    Parameters
    ----------
    klass : class
        class to search

    Returns
    -------
    all_parents : list
        all the parent types
    """
    all_parents = []
    for parent_klass in klass.__bases__:
        if parent_klass not in all_parents:
            all_parents.append(parent_klass)
            all_parents.extend(get_parent_types(parent_klass))
    return all_parents


def get_parser_class(tuple_obj: tuple) -> bool:
    """
    Get parser class from a module.

    Parameters
    ----------
    tuple_obj : tuple
        tuple which contains name of the module and the associated module object

    Returns
    -------
    parser_or_not : bool
        True if the class is inherite of the `Parser` class, False otherwise

    See also
    --------
    Parser, get_parent_types
    """
    _, klass = tuple_obj
    return Parser in get_parent_types(klass)

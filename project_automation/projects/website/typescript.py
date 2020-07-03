import os
from typing import Any, NoReturn

from project_automation.exceptions import TypescriptCommandNotExists
from project_automation.files import Folder, CSSFile, HTMLFile, TypescriptFile
from project_automation.projects import Project
from project_automation.utils import execute_command, execute_command2


class TypescriptWebsiteProject(Project):
    """
    Represents the base of a Typescript website project to create.

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
        'languages': ["HTML", "CSS", "JavaScript", "Typescript"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Compile the typescript](#compilation)"),
            '3': ("title", "Compilation", 2),
            '4': ("code", "$ tsc js/script.ts", "shell"),
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
        super().__init__(path, name, github_settings=github_settings)

    def create(self) -> NoReturn:
        """
        Create the structure of the project.
        """
        super().create()
        # Create the JS folder and JS files
        js_dir = Folder(os.path.join(self.path, "js"))
        script = TypescriptFile(os.path.join(self.path, "js"), "script")
        js_dir.add(script)

        # Create the CSS folder and CSS files
        css_dir = Folder(os.path.join(self.path, "style"))
        style = CSSFile(os.path.join(self.path, "style"), "style")
        css_dir.add(style)

        # Create other folders
        assets_dir = Folder(os.path.join(self.path, "assets"))
        images_dir = Folder(os.path.join(
            os.path.join(self.path, "assets"), "images"))
        fonts_dir = Folder(os.path.join(
            os.path.join(self.path, "assets"), "fonts"))
        assets_dir.add(images_dir, fonts_dir)

        # Create some files
        index_html_file = HTMLFile(self.path, "index")
        index_html_file.add_headlink(
            type="text/css", rel="stylesheet", href=style.filename, href_is_relative=False)
        index_html_file.add_script(src=script.filename, src_is_relative=False)
        self.root.add(index_html_file, js_dir, css_dir, assets_dir)

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        super().verify_installation()
        code, _, _ = execute_command(
            f"tsc --version")
        if code:
            raise TypescriptCommandNotExists(allow_install=self.allow_install)

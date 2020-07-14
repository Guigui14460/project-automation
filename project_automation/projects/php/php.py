import os
from typing import Any, NoReturn

from project_automation.commands import PHPCommand
from project_automation.files import Folder, CSSFile, HTMLFile, JavascriptFile, JSONFile, PHPFile
from project_automation.projects import Project


class PHPWebsiteProject(Project):
    """
    Represents the base of a simple website project to create.

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
        'languages': ["HTML", "CSS", "JavaScript", "PHP"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ("code", "$ php -S localhost:8000", "shell"),
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
        super().__init__(path, name, github_settings=github_settings, **kwargs)

    def create(self) -> NoReturn:
        """
        Create the structure of the project.
        """
        super().create()
        composer_json_file = JSONFile(self.path, 'composer')
        composer_json_file.write({
            "name": "pds/skeleton",
            "type": "standard",
            "description": "Standard for PHP package skeletons.",
            "homepage": "https://github.com/php-pds/skeleton",
            "license": "CC-BY-SA-4.0",
            "autoload": {
                "psr-4": {
                    "Pds\\Skeleton\\": "src/"
                }
            },
            "autoload-dev": {
                "psr-4": {
                    "Pds\\Skeleton\\": "tests/"
                }
            },
            "bin": ["bin/pds-skeleton"]
        })
        self.root.add(composer_json_file)

        bin_dir = Folder(os.path.join(self.path, "bin"))
        config_dir = Folder(os.path.join(self.path, "config"))
        docs_dir = Folder(os.path.join(self.path, "docs"))
        public_dir = Folder(os.path.join(self.path, "public"))
        src_dir = Folder(os.path.join(self.path, "src"))
        ressources_dir = Folder(os.path.join(self.path, "ressources"))
        src_dir = Folder(os.path.join(self.path, "src"))
        tests_dir = Folder(os.path.join(self.path, "tests"))
        vendor_dir = Folder(os.path.join(self.path, "vendor"))
        self.root.add(bin_dir, config_dir, docs_dir, public_dir,
                      src_dir, ressources_dir, tests_dir, vendor_dir)

        # Create the JS folder and JS files
        js_dir = Folder(os.path.join(self.path, "src", "js"))
        script = JavascriptFile(os.path.join(self.path, "src", "js"), "script")
        js_dir.add(script)

        # Create the CSS folder and CSS files
        css_dir = Folder(os.path.join(self.path, "src", "style"))
        style = CSSFile(os.path.join(self.path, "src", "style"), "style")
        css_dir.add(style)

        # Create other folders
        assets_dir = Folder(os.path.join(self.path, "src", "assets"))
        images_dir = Folder(os.path.join(self.path, "src", "assets", "images"))
        fonts_dir = Folder(os.path.join(self.path, "src", "assets", "fonts"))
        assets_dir.add(images_dir, fonts_dir)

        # Create some files
        index_html_file = HTMLFile(os.path.join(self.path, "src"), "index")
        index_html_file.add_headlink(
            type="text/css", rel="stylesheet", href=style.filename, href_is_relative=False)
        index_html_file.add_script(src=script.filename, src_is_relative=False)
        index_html_file.write_xml()
        php_file = PHPFile(os.path.join(self.path, "src"), "index")
        # Transfert the HTML content to PHP file
        content = index_html_file.read()
        start_H1 = content.find("<h1>")
        end_H1 = content.find("</h1>")
        # Change the H1 tag
        content2 = content[:start_H1 + len("<h1>")] + \
            "<?php echo \"Hello World\"; ?>" + content[end_H1:]
        php_file.write(content2)
        # Delete the HTML file
        index_html_file.remove()
        src_dir.add(php_file, js_dir, css_dir, assets_dir)

    def verify_installation(self):
        """
        Verify if all the required programs are installed.

        See also
        --------
        commands.PHPCommand
        """
        super().verify_installation()
        PHPCommand(self.allow_install)

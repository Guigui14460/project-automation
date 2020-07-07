import os
import sys
from typing import Any, NoReturn

from project_automation.commands import JavaCommand, JavacCommand
from project_automation.files import Folder, JavaFile, BashFile, BatchFile, TextFile
from project_automation.projects import Project
from project_automation.utils import execute_command


class JavaProject(Project):
    """
    Represents the base of a Java project to create.

    Attributes
    ----------
    path : str
        path of the parent root of the project
    name : str
        name of the project (used for make directory and github repo)
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    package_name : str
        name of the package to put at the head of the Java files
    company_name : str
        name of the company (for the name of the package and maven)
    executing_scripts : bool
        allows us to create scripts to simplify the usage
    generate_files : bool
        use to generate the file or not
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
        'languages': ["Java"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '5': ("code", "$ javac -encoding \"utf-8\" -d build/ src/*.java", "shell"),
            '6': ("code", "$ java -cp build main.Main [args ...]", "shell"),
        },
    }

    def __init__(self, path: str, name: str, package_name: str, company_name: str, executing_scripts: bool = True, generate_files: bool = True, github_settings: dict = {}, **kwargs: Any) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the parent root of the project
        name : str
            name of the project (used for make directory and github repo)
        package_name : str
            name of the package to put at the head of the Java files
        company_name : str
            name of the company (for the name of the package and maven)
        executing_scripts : bool
            allows us to create scripts to simplify the usage
        generate_files : bool
            use to generate the file or not
        github_settings : dict
            some github informations
        **kwargs : Any
            other keywords parameters
        """
        super().__init__(path, name, github_settings=github_settings, **kwargs)
        self.executing_scripts = executing_scripts
        self.package_name = package_name
        self.company_name = company_name
        self.generate_files = generate_files
        if self.executing_scripts and self.generate_files:
            self.CONFIG['readme_content'].update({'4': ('paragraph', 'For Unix-like systems :'),
                                                  '5': ("code", "$ sh run.sh", "shell"),
                                                  '6': ('paragraph', 'For Windows systems :'),
                                                  '7': ("code", "$ run.bat", "powershell"), })

    def create(self) -> NoReturn:
        """
        Create the structure of the project.
        """
        super().create()
        if self.generate_files:
            if self.executing_scripts:
                name = self.company_name
                if self.company_name == 'nobody' and self.user is not None:
                    name = self.user.name
                manifest_file = TextFile(self.path, 'Manifest')
                manifest_file.write(
                    f"Main-Class: {self.package_name}.Main\nManifest-Version: 1.0\nCreated-By: {name}")

                compile_script_content = f"javac -encoding \"utf-8\" -d build/ src/{self.package_name}/*.java"
                compile_bash_script = BashFile(self.path, 'compile')
                compile_bash_script.write(compile_script_content)
                compile_batch_script = BatchFile(self.path, 'compile')
                compile_batch_script.write(compile_script_content)
                self.root.add(compile_bash_script, compile_batch_script)

                if sys.platform == 'win32':
                    run_script_content = "call compile.bat"
                else:
                    run_script_content = "sh compile.sh"
                run_script_content += f"\njava -cp build {self.package_name}.Main"
                run_bash_script = BashFile(self.path, 'run')
                run_bash_script.write(run_script_content)
                run_batch_script = BatchFile(self.path, 'run')
                run_batch_script.write(run_script_content)
                self.root.add(run_bash_script, run_batch_script)

                doc_script_content = f"javadoc -encoding \"utf-8\" -docencoding \"utf-8\" -d doc/ src/{self.package_name}/*.java "
                doc_bash_script = BashFile(self.path, 'doc')
                doc_bash_script.write(doc_script_content)
                doc_batch_script = BatchFile(self.path, 'doc')
                doc_batch_script.write(doc_script_content)
                self.root.add(doc_bash_script, doc_batch_script)

                if sys.platform == 'win32':
                    package_script_content = "call compile.bat"
                else:
                    package_script_content = "sh compile.sh"
                package_script_content += f"\ncd build/\njar cfm {self.package_name}.jar \"../Manifest.txt\" {self.package_name}/\ncd ..\nmkdir dist\n"
                if sys.platform == 'win32':
                    package_script_content += f"move \"build\{self.package_name}.jar\" dist/"
                else:
                    package_script_content += f"mv build/{self.package_name}.jar dist/{self.package_name}.jar"
                package_bash_script = BashFile(self.path, 'package')
                package_bash_script.write(package_script_content)
                package_batch_script = BatchFile(self.path, 'package')
                package_batch_script.write(package_script_content)
                self.root.add(package_bash_script, package_batch_script)

            package_path = os.path.join(
                self.path, 'src', self.package_name)
            package_dir = Folder(package_path)
            java_file = JavaFile(package_path, "Main", self.package_name)

            package_info_file = JavaFile(
                package_path, "package-info", self.package_name)
            package_info_file.write(f"""/**
* <b>Description : </b> Packages organisation for the project.
* 
* @author {self.company_name}
* 
* @version 0.1
*/""")
            self.root.add(java_file, package_info_file)

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        super().verify_installation()
        JavaCommand(self.allow_install)
        JavacCommand(self.allow_install)

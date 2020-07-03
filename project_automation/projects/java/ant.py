import os
import shutil
from typing import Any, NoReturn
from xml.etree import ElementTree as ET

from project_automation.commands import AntCommand
from project_automation.files import JavaFile, BatchFile, BashFile, Folder, XMLFile
from project_automation.projects.java.java import JavaProject
from project_automation.utils import execute_command


class AntProject(JavaProject):
    """
    Represents the base of a Java project with Ant to create.

    Attributes
    ----------
    path : str
        path of the parent root of the project
    name : str
        name of the project (used for make directory and github repo)
    allow_install : bool
        True if you want to automatically install the required packages, False otherwise
    package_name : str
        name of the app to put at the head of the Java files
    company_name : str
        name of the company (for the name of the package and maven)
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
        'languages': ["Java", "Ant", "XML"],
        'readme_content': {
            '1': ("title", "Table of contents", 2),
            '2': ("paragraph", "1. [Usage of the application](#usage)"),
            '3': ("title", "Usage", 2),
            '4': ("code", "$ ant <cmd>", "shell"),
        },
    }

    def __init__(self, path: str, name: str, package_name: str, company_name: str, github_settings: dict = {}, **kwargs) -> NoReturn:
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
        github_settings : dict
            some github informations
        **kwargs : Any
            other keywords parameters
        """
        super().__init__(path, name, package_name, company_name,
                         executing_scripts=False, generate_files=False, github_settings=github_settings, **kwargs)

    def create(self) -> NoReturn:
        """
        Create the structure of the project.
        """
        super().create()
        package = '.'.join([self.company_name.lower(), self.package_name])
        # Src directory
        main_path = os.path.join(
            self.path, 'src', 'main', 'java', self.company_name.lower(), self.package_name)
        main_resources_path = os.path.join(
            self.path, 'src', 'main', 'resources')
        test_path = os.path.join(
            self.path, 'src', 'test', 'java', self.company_name.lower(), self.package_name)
        test_resources_path = os.path.join(
            self.path, 'src', 'test', 'resources')
        main_dir = Folder(main_path)
        test_dir = Folder(test_path)
        self.root.add(main_dir, test_dir, Folder(
            main_resources_path), Folder(test_resources_path))

        # Lib directory
        self.root.add(Folder(os.path.join(self.path, 'lib')))

        java_file = JavaFile(main_path, "Main", package)
        package_info_file = JavaFile(
            main_path, "package-info", package)
        package_info_file.write(f"""/**
* <b>Description : </b> Packages organisation for the project.
* 
* @author {self.company_name}
* 
* @version 0.1
*/""")
        main_dir.add(java_file, package_info_file)
        java_test_file = JavaFile(test_path, "MainTest", package)
        java_test_file.write(f"""package {package};

public class MainTest {{
    private static void testHelloWorld(){{
        assert Main.helloWorld() == "Hello World";
    }}

    public static void main(String[] args){{
        testHelloWorld();
    }}
}}
""")
        test_dir.add(java_test_file)

        build = XMLFile(self.path, 'build')
        build.root = ET.Element(
            "project", attrib={"name": self.name, "default": "run", "basedir": "."})
        # All variables
        ET.SubElement(build.root, "property", attrib={
                      "name": "src.dir", "value": f"${{basedir}}/src/main/java/{self.company_name.lower()}/{self.package_name.lower()}"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "src.resources.dir", "value": "${basedir}/src/main/resources"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "test.dir", "value": f"${{basedir}}/src/test/java/{self.company_name.lower()}/{self.package_name.lower()}"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "test.resources.dir", "value": "${basedir}/src/test/resources"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "bin.dir", "value": "${basedir}/bin"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "bin.main.dir", "value": "${basedir}/bin/main/"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "bin.test.dir", "value": "${basedir}/bin/test/"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "docs.dir", "value": "${basedir}/docs"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "dist.dir", "value": "${basedir}/dist"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "lib.dir", "value": "${basedir}/lib"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "main.class", "value": f"{package}.Main"})
        ET.SubElement(build.root, "property", attrib={
                      "name": "main.test.class", "value": f"{package}.MainTest"})
        # Use to simplify commands with the external jar files
        path_ele = ET.SubElement(build.root, "path", attrib={
                                 "id": "project.classpath"})
        fileset = ET.SubElement(path_ele, "fileset", attrib={
                                "dir": "${lib.dir}"})
        ET.SubElement(fileset, "include", attrib={"name": "*.jar"})
        ET.SubElement(fileset, "include", attrib={"name": "*.dll"})
        ET.SubElement(fileset, "include", attrib={"name": "*.so"})
        ET.SubElement(path_ele, "fileset", attrib={
                                "dir": "${src.resources.dir}"})
        ET.SubElement(path_ele, "pathelement", attrib={
                      "location": "${bin.main.dir}"})
        ET.SubElement(path_ele, "fileset", attrib={
                                "dir": "${test.resources.dir}"})
        ET.SubElement(path_ele, "pathelement", attrib={
                      "location": "${bin.test.dir}"})
        # clean command
        clean_target = ET.SubElement(build.root, "target", attrib={
            "name": "clean", "description": "Classes compiling", "depends": ""})
        ET.SubElement(clean_target, "delete", attrib={"dir": "${bin.dir}"})
        ET.SubElement(clean_target, "delete", attrib={"dir": "${dist.dir}"})
        # compile command
        compile_target = ET.SubElement(build.root, "target", attrib={
                                       "name": "compile", "description": "Classes compiling", "depends": ""})
        ET.SubElement(compile_target, "mkdir", attrib={
                      "dir": "${bin.main.dir}"})
        javac_compile_target = ET.SubElement(compile_target, "javac", attrib={
                                             "Encoding": "utf-8", "srcdir": "${src.dir}", "destdir": "${bin.main.dir}", "debug": "on", "optimize": "off", "deprecation": "on", "includeantruntime": "false", "modulepath": "${lib.dir}"})
        ET.SubElement(javac_compile_target, "classpath",
                      attrib={"refid": "project.classpath"})
        # run command
        run_target = ET.SubElement(build.root, "target", attrib={
                                   "name": "run", "description": "Execution", "depends": "compile"})
        java_run_target = ET.SubElement(run_target, "java", attrib={
                                        "classname": "${main.class}", "fork": "true", "modulepath": "${lib.dir}"})
        ET.SubElement(java_run_target, "classpath", attrib={
                      "refid": "project.classpath"})
        # runpackage command
        runpackage_target = ET.SubElement(build.root, "target", attrib={
                                          "name": "runpackage", "description": "Execution", "depends": "packaging"})
        java_runpackage_target = ET.SubElement(runpackage_target, "java", attrib={
                                               "jar": "${dist.dir}/${ant.project.name}.jar", "fork": "true", "modulepath": "${lib.dir}"})
        ET.SubElement(java_runpackage_target, "classpath",
                      attrib={"refid": "project.classpath"})
        # doc command
        doc_target = ET.SubElement(build.root, "target", attrib={
                                   "name": "doc", "description": "Generate the javadoc"})
        ET.SubElement(doc_target, "mkdir", attrib={"dir": "${docs.dir}"})
        javadoc_doc_target = ET.SubElement(doc_target, "javadoc", attrib={
                                           "Encoding": "utf-8", "windowtitle": "${ant.project.name}", "useexternalfile": "true", "use": "true", "access": "private", "sourcepath": "${src.dir}", "destdir": "${docs.dir}"})
        fileset_doc = ET.SubElement(javadoc_doc_target, "fileset", attrib={
                                    "dir": "${src.dir}", "defaultexcludes": "yes"})
        ET.SubElement(fileset_doc, "include", attrib={"name": "*.java"})
        ET.SubElement(javadoc_doc_target, "classpath",
                      attrib={"refid": "project.classpath"})
        # packaging command
        packaging_target = ET.SubElement(build.root, "target", attrib={
            "name": "packaging", "description": "Packaging the project", "depends": "compile"})
        ET.SubElement(packaging_target, "mkdir", attrib={"dir": "${dist.dir}"})
        jar_packaging_target = ET.SubElement(packaging_target, "jar", attrib={
            "jarfile": "${dist.dir}/${ant.project.name}.jar", "basedir": "${bin.main.dir}"})
        ET.SubElement(jar_packaging_target, "zipgroupfileset", attrib={
                      "dir": "${lib.dir}", "includes": "*.jar"})
        manifest_ele = ET.SubElement(jar_packaging_target, "manifest")
        ET.SubElement(manifest_ele, "attribute", attrib={
                      "name": "Manifest-Version", "value": "1.0"})
        ET.SubElement(manifest_ele, "attribute", attrib={
                      "name": "Created-By", "value": f"{self.company_name}"})
        ET.SubElement(manifest_ele, "attribute", attrib={
                      "name": "Main-Class", "value": "${main.class}"})
        # test command
        test_target = ET.SubElement(build.root, "target", attrib={
            "name": "test", "description": "Test the project", "depends": ""})
        ET.SubElement(test_target, "mkdir", attrib={"dir": "${bin.test.dir}"})
        javac_test_target = ET.SubElement(test_target, "javac", attrib={
            "Encoding": "utf-8", "srcdir": "${test.dir}", "destdir": "${bin.test.dir}", "debug": "on", "optimize": "off", "deprecation": "on", "includeantruntime": "false", "modulepath": "${lib.dir}"})
        ET.SubElement(javac_test_target, "classpath",
                      attrib={"refid": "project.classpath"})
        java_test_target = ET.SubElement(test_target, "java", attrib={
            "classname": "${main.test.class}", "fork": "true", "modulepath": "${lib.dir}"})
        ET.SubElement(java_test_target, "classpath", attrib={
                      "refid": "project.classpath"})
        ET.SubElement(java_test_target, "jvmarg", attrib={"value": "-ea"})
        build.write_xml()

    def verify_installation(self) -> NoReturn:
        """
        Verify if all the required programs are installed.

        See also
        --------
        utils.execute_command
        """
        super().verify_installation()
        AntCommand(self.allow_install)

from typing import NoReturn

from project_automation.files import CustomFileExtension


class JavaFile(CustomFileExtension):
    """
    Represents a `.java` file.

    Attributes
    ----------
    filename : str
        represents the path of the file and his name (with the extension)
    """

    CONFIG = {
        "extension": "java"
    }

    def __init__(self, path: str, filename: str, package_name: str) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the file (not add the filename)
        filename : str
            name of the file without extension
        package_name : str
            name of the main package
        """
        self.package_name = package_name
        super().__init__(path, filename)

    def init(self) -> NoReturn:
        """
        Initialize the content of the file.
        """
        content = f"""package {self.package_name};

public class Main {{
    public static String helloWorld(){{
        String str = "Hello World";
        System.out.println(str);
        return str;
    }}

    public static void main(String[] args){{
        helloWorld();
    }}
}}
"""
        self.write(content)

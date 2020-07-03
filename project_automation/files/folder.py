import os
import shutil
from typing import Iterable, NoReturn


class Folder:
    """
    Represents a folder which contains some files and folder.

    Attributes
    ----------
    path : str
        path of the folder
    files : iterable of files/folder objects
        list of files and folder
    """

    def __init__(self, path: str, *files: Iterable) -> NoReturn:
        """
        Constructor and initializer.

        Parameters
        ----------
        path : str
            path of the folder
        *files : tuple of files/folder objects
            list of files and folder
        """
        self.path = path
        self.files = [*files]
        self.create()

    def create(self) -> NoReturn:
        """
        Create root folder and recursively subfiles and subfolders.
        """
        os.makedirs(self.path, exist_ok=True)
        for file in self.files:
            file.create()

    def add(self, *files: Iterable) -> NoReturn:
        """
        Add files and folder.

        Parameters
        ----------
            *files : iterable
                tuple of files and folders
        """
        self.files.extend(files)

    def remove(self, *files: Iterable) -> NoReturn:
        """
        Remove files and folder.

        Parameters
        ----------
            *files : iterable
                tuple of files and folders
        """
        for file in self.files:
            self.files.remove(file)

    def remove_folder(self) -> NoReturn:
        """
        Remove folder and all subfiles/subfolders.
        """
        before_path, current_dir = os.path.split(self.path)
        os.chdir(before_path)
        shutil.rmtree(current_dir)

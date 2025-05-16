from typing import Generator, Iterable
import os


import os
from typing import Generator, Iterable

class FileManager:
    """
    Handles basic file management operations within a specified directory.

    The FileManager class provides utilities to:
    - List files in a given directory with filtering options.
    - Write iterable content to a file, creating directories as needed.

    Attributes:
        __base_path (str): The root directory used for file operations.
    """

    __base_path: str

    def __init__(self, dir_path: str):
        """
        Initializes the FileManager with a base directory.

        Args:
            dir_path (str): Path to the directory for file operations.
        """
        self.__base_path = dir_path

    def list_files(
        self, ignore_extensions: list[str] = None, show_path: bool = False
    ) -> Generator:
        """
        Lists files in the base directory, optionally filtering by file 
        extension and showing full paths.

        Args:
            ignore_extensions (list[str], optional): A list of file extensions 
                to ignore (e.g., [".c"]). Defaults to [".c"].
            show_path (bool, optional): If True, yields full file paths. If 
                False, yields only file names. Defaults to False.

        Yields:
            Generator[str, None, None]: A generator that yields file names or 
                paths.
        """
        if ignore_extensions is None:
            ignore_extensions = [".c"]

        for file_name in os.listdir(self.__base_path):
            _, extension = os.path.splitext(file_name)

            if (os.path.isdir(f"./{file_name}") or 
                extension in ignore_extensions):
                continue
        
            if show_path:
                yield f"{self.__base_path}/{file_name}"
            else:
                yield file_name

    def write_generator(self, path: str, rows: Iterable) -> None:
        """
        Writes a sequence of rows to a file, creating directories if necessary.

        Args:
            path (str): The full file path to write to.
            rows (Iterable): An iterable of rows (typically strings) to write 
                into the file.

        Side Effects:
            - Creates the target directory if it does not exist.
            - Overwrites the file if it already exists.
        """
        dir_path, _ = os.path.split(path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        with open(path, "w") as file:
            for row in rows:
                file.write(f"{row}\n")

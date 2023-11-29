"""
Folder class that details a directory
"""

from typing import TypeVar  # For use in type hinting
from copy import deepcopy  # For use in crafting

# Type Declarations
T = TypeVar('T')  # generic type
Dir = TypeVar('Dir')  # forward declared

class Directory:
    """
    Implementation of a directory
    """

    __slots__ = ['name', 'files']

    def __init__(self, name: str) -> None:
        """
        Initializes a directory
        :return: None
        """
        self.name = name
        self.files = []

    def __repr__(self) -> str:
        """
        Represents a `Directory` as a string
        """
        return self.to_string()

    def __str__(self) -> str:
        """
        Represents a `Directory` as a string
        """
        return self.to_string()

    def __eq__(self, other: Dir) -> bool:
        """
        Overloads `==` operator to compare Directories
        :param other: right hand operand of `==`
        :return: `True` if equal, else `False`
        """
        return str(self) == str(other)


    def to_string(self) -> str:
        """
        String conversion of directory
        :return: string representation of Directory
        """
        res = self.name + " -> "

        res += str(self.files)
        return res

    def add_file(self, file: str):
        self.files.append(file)

    def add_dir(self, directory: Dir):
        self.files.append(directory)


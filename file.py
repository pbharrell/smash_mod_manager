"""
File class that details a file
"""

from typing import TypeVar  # For use in type hinting
from copy import deepcopy  # For use in crafting

# Type Declarations
T = TypeVar('T')  # generic type
Dir = TypeVar('Dir')  # forward declared

class File:
    """
    Implementation of a file
    """

    __slots__ = ['name', 'path']

    def __init__(self, name: str) -> None:
        """
        Initializes a file
        :return: None
        """
        self.name = name
        self.path = []

    def __repr__(self) -> str:
        """
        Represents a `File` as a string
        """
        return self.to_string()

    def __str__(self) -> str:
        """
        Represents a `File` as a string
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
        String conversion of file
        :return: string representation of file
        """
        res = self.name + " -> "

        res += str(self.path)
        return res

    def add_to_path(self, file: str):
        self.path.append(file)


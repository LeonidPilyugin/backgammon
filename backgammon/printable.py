# printable.py
# Contains Printable class

from abc import ABCMeta, abstractmethod


class Printable(metaclass=ABCMeta):
    """Printable class
    Describes printable object
    
    Methods:
        1) print(): prints object
    """

    @abstractmethod
    def print(self) -> None:
        """Prints object"""
        pass

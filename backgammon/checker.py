# checker.py
# Contains Checker class

import pygame
from typing import Tuple
from visible import Visible

class Checker(Visible):
    """Checker(Visible) class
    Describes a checker
    
    Methods:
        1) print(): prints object
        2) throw(): throws checker
    
    Properties:
        1) color: color of checker
        
    Constants:
        1) TYPES: possible types for checker ("red" or "black")
    """
    TYPES = ("red", "black")
    
    def __init__(self, screen: pygame.Surface, checker_color: str,
                 position: Tuple[int], size: Tuple[int]) -> None:
        """Constructor of Checker

        Args:
            screen (pygame.Surface): screen to print on
            checker_color (str): color of checker, must be in Checker.TYPES
            position (Tuple[int]): position of checker
            size (Tuple[int]): size ofchecker
        """
        # set color
        self._color = checker_color
        # set screen
        self._screen = screen
        # set position
        self._position = position
        # set size
        self._size = size
        # load image
        self._load_image(f"images/{self._color}.png")
        
    @property
    def color(self) -> str:
        """Color of checker

        Returns:
            str: color of checker
        """
        return self._color

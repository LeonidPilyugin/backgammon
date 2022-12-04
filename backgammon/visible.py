# visible.py
# Contains Visible class

import pygame
from abc import ABCMeta
from printable import Printable

class Visible(Printable, metaclass=ABCMeta):
    """Visible(Printable) class
    Describes an image printable object
    
    Methods:
        1) print(): prints object
    """
    
    def _load_image(self, image_path: str) -> None:
        """Loads image to memory

        Args:
            image_path (str): path to loading image
        """
        self._image = pygame.image.load(image_path)
        self._image = pygame.transform.scale(self._image, self._size)
    
    def print(self) -> None:
        """Prints object"""
        self._screen.blit(self._image, self._position)

# visible.py
# Contains Visible class

from abc import ABCMeta

import pygame

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
        
        self._image = pygame.image.load(image_path)  # load image
        self._image = pygame.transform.scale(self._image, self._size)  # scale image

    def print(self) -> None:
        """Prints object"""
        
        self._screen.blit(self._image, self._position)  # print image

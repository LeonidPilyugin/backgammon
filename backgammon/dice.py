# dice.py
# Contains Dice class

from random import randint
from typing import Tuple

import pygame

from visible import Visible


class Dice(Visible):
    """Dice(Visible) class
    Describes a dice
    
    Methods:
        1) print(): prints object
        2) throw(): throws dice
    Properties:
        1) value: value of dice
    """

    def __init__(self, screen: pygame.Surface,
                 position: Tuple[int, int], size: Tuple[int, int]) -> None:
        """Dice constructor

        Args:
            screen (pygame.Surface): surface to print on
            position (Tuple[int]): position of dice
            size (Tuple[int]): size of dice
        """
        # set screen
        self._screen = screen
        # set position
        self._position = position
        # set size
        self._size = size
        # load image
        self._load_image()
        # throw
        self.throw()

    def _load_image(self, path=None) -> None:
        # load each of 6 planes
        self._images = []
        for i in range(1, 7):
            self._images.append(None)
            self._images[-1] = pygame.image.load(f"images/dice{i}.png")
            self._images[-1] = pygame.transform.scale(self._images[-1], self._size)

    def throw(self) -> None:
        # set random value from 1 to 6
        self._value = randint(1, 6)

    def print(self) -> None:
        # print image of current value
        self._screen.blit(self._images[self._value - 1], self._position)

    @property
    def value(self) -> int:
        """Value of dice

        Returns:
            int: value of dice
        """
        return self._value

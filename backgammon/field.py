# field.py
# Contains Field class

from threading import Lock
from typing import Tuple

import pygame

from abstractplayer import AbstractPlayer
from cell import Cell
from dice import Dice
from visible import Visible


class Field(Visible):
    """Field(Visible) class
    Describes backgammon field
    
    Methods:
        1) start(): starts game
        2) print(): prints field
    """

    def __init__(self, screen: pygame.Surface, size: Tuple[int, int],
                 players: Tuple[AbstractPlayer]) -> None:
        """Field constructor

        Args:
            screen (pygame.Surface): surface to print on
            size (Tuple[int]): size of field image
            players (Tuple[AbstractPlayer]): 2-element tuple of players
        """
        
        self._screen = screen  # set screen
        self._position = (0, 0)  # set position
        self._size = size  # set size
        
        self._load_image("images/field.png")  # load image
        
        self._dices = [Dice(screen, (200 + 100 * i, 450), (40, 40)) \
            for i in range(2)]  # list of two dices
        
        self._cells = [Cell(self._screen,
                            i,
                            15 if i == 0 or i == 12 else 0,
                            "red" if i == 0 else "black"
                            if i == 12 else "") \
                                for i in range(0, 26)] # list of 26 cells (24 main and 2 of exited checkers)
        
        self._players = players  # players tuple
        
        self._cell_locker = Lock()  # cells locker

    def start(self) -> None:
        """Starts game"""
        
        while len(self._cells[24]) < 15 and len(self._cells[25]) < 15:  # while there are checkers of both colors, play game
            self._throw_dices()  # throw dices
            
            self._players[0].play([self._dices[0].value, self._dices[1].value])  # next players plays
            
            # if double, throw one more time
            if self._dices[0].value == self._dices[1].value:
                continue
            
            self._players = self._players[1:] + self._players[:1]  # shift players

    def _throw_dices(self) -> None:
        """Throws each dice"""
        
        # throw each dice
        for dice in self._dices:
            dice.throw()

    def print(self) -> None:
        """Prints field"""
        
        super().print()  # print background
        
        # print dices
        for dice in self._dices:
            dice.print()
        
        # print cells
        for cell in self._cells:
            cell.print()

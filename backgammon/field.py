# field.py
# Contains Field class

import pygame
from typing import Tuple
from threading import Lock
from visible import Visible
from cell import Cell
from dice import Dice
from abstractplayer import AbstractPlayer

class Field(Visible):
    """Field(Visible) class
    Describes backgammon field
    
    Methods:
        1) start(): starts game
        2) print(): prints field
    """
    
    def __init__(self, screen: pygame.Surface, size: Tuple[int],
                 players: Tuple[AbstractPlayer]) -> None:
        """Field constructor

        Args:
            screen (pygame.Surface): surface to print on
            size (Tuple[int]): size of field image
            players (Tuple[AbstractPlayer]): 2-element tuple of players
        """
        # set screen
        self._screen = screen
        # set position
        self._position = (0, 0)
        # set size
        self._size = size
        # load image
        self._load_image("images/field.png")
        # list of two dices
        self._dices = [Dice(screen, (200 + 100 * i, 450), (40, 40)) for i in range(2)]
        # list of 26 cells (24 main and 2 of exited checkers)
        self._cells = [Cell(self._screen,
                            i,
                            15 if i == 0 or i == 12 else 0,
                            "red" if i == 0 else "black" \
                                if i == 12 else "") for i in range(0, 26)]
        # players tuple
        self._players = players
        # cells locker
        self._cell_locker = Lock()
        
    def start(self) -> None:
        """Starts game"""
        # while there are checkers of both colors, play game
        while(len(self._cells[24]) < 15 or len(self._cells[25] < 15)):
            # throw dices
            self._throw_dices()
            # next players plays
            self._players[0].play([self._dices[0].value, self._dices[1].value])
            # if double, throw one more time
            if self._dices[0].value == self._dices[1].value:
                continue
            # shift players
            self._players = self._players[1:] + self._players[:1]
            
    def _throw_dices(self) -> None:
        """Throws each dice"""
        # throw each dice
        for dice in self._dices:
            dice.throw()
        
            
    def print(self) -> None:
        """Prints field"""
        # print background
        super().print()
        # print dices
        for dice in self._dices:
            dice.print()
        # print cells
        with self._cell_locker:
            for cell in self._cells:
                cell.print()
        
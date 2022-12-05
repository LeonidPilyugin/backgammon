# cell.py
# Contains Cell and CellIter classes

from typing import Tuple

import pygame

from checker import Checker
from printable import Printable


class Cell(Printable):
    """Cell(Visible) class
    Describes a backgammon field's cell
    
    Cell is indexable, iterable and has lenght
    
    Methods:
        1) print(): prints object
        2) highlight(color: str): sets highlight color
        3) move_checker(cell: Cell) moves checker to other cell
        4) isinside(position: Tuple[int]): returns True if position is inside cell
    
    Properties:
        1) color: color of highlight
        2) index: index on field
        
    Constants:
        1) COLORS: dictionary of possible highlighting colors
    """

    # dictionary of highlighting colors
    COLORS = {"hover": "#f0f0f0", "selected": "#ffff00", "suggest": "#00ff00", None: None}
    # size
    _SIZE = (54, 376)
    # tuple of x cells' and checkers' coordinates
    _XS = [120, 175, 235, 290, 350, 405, 540, 600, 660, 720, 775, 835]
    _XS.extend(reversed(_XS))
    _X0S = [-10, 930]
    _XS.extend(_X0S)
    _XS = tuple(_XS)
    # tuple of y checkers' coordinates
    _YS = list(reversed(range(505, 786, 20)))
    _YS.extend(list(range(85, 366, 20)))
    _YS = tuple(_YS)

    def __init__(self, screen: pygame.Surface, index: int, checkers: int, color: str) -> None:
        """Cell constructor

        Args:
            screen (pygame.Surface): surface to print on
            index (int): index on field of this cell
            checkers (int): number of checkers in cell
            color (str): color of checkers
        """
        # set screen
        self._screen = screen
        # set size
        self._size = Cell._SIZE
        # set index
        self._index = index
        # set position
        self._position = (Cell._XS[index], 85 if index == 24
        else 460 if index == 25 else 460 if index < 12 else 85)
        # set highlight color
        self._color = None
        # insert checkers
        self._checkers = []
        for _ in range(checkers):
            self._push_checker(color)

    def __iter__(self):
        """Returns iterator of this cell (iterates throw checkers)

        Returns:
            CellIterator: iterator
        """
        return CellIter(self)

    def __len__(self) -> int:
        """Returns number of checkers

        Returns:
            int: number of checkers
        """
        return len(self._checkers)

    def __getitem__(self, key: int) -> Checker:
        """Returns checker by index (like in list)

        Args:
            key (int): index

        Returns:
            Checker: checker by index
        """
        return self._checkers[key]

    @property
    def color(self) -> str:
        """Highlight color

        Returns:
            str: color of highlight
        """
        return self._color

    @property
    def index(self) -> int:
        """Index of cell on field

        Returns:
            int: index of cell on field
        """
        return self._index

    def highlight(self, value: str) -> None:
        """Sets highlight color by key in Cell.COLORS

        Args:
            value (str): key in Cell.COLORS

        Raises:
            ValueError: in case of value not in keys of Cell.COLORS
        """
        if value not in Cell.COLORS.keys():
            raise ValueError("Value is incorrect")
        self._color = Cell.COLORS[value]

    def move_checker(self, cell) -> None:
        """Moves checker to other cell

        Args:
            cell (_type_): cell to move checker to
        """
        cell._push_checker(self._pop_checker().color)

    def _push_checker(self, color: str) -> None:
        """Adds checker to this cell

        Args:
            color (str): color of adding checker
        """
        self._checkers.append(Checker(self._screen, color,
                                      (self._position[0],
                                       Cell._YS[len(self._checkers) + 15 * (self._index - 24)] if self._index > 23 else
                                       Cell._YS[len(self._checkers) + 15 * (self._index // 12)]),
                                      (50, 50)))

    def _pop_checker(self) -> Checker:
        """Pops checker from this cell

        Returns:
            Checker: poped checker
        """
        return self._checkers.pop()

    def print(self) -> None:
        # print all checkers
        for ch in self._checkers:
            ch.print()
        # highligth cell if necessary
        if self._color is not None:
            pygame.draw.rect(self._screen, self._color,
                             (self._position[0], self._position[1],
                              self._size[0], self._size[1]), 5)

    def isinside(self, position: Tuple[int]) -> bool:
        """Returns True if position is inside cell, else False

        Args:
            position (Tuple[int]): tuple of lenght 2

        Returns:
            bool: True if position is inside cell, else False
        """
        return self._position[0] < position[0] < self._position[0] + self._size[0] and \
               self._position[1] < position[1] < self._position[1] + self._size[1]


class CellIter:
    """Cell iterator object"""

    def __init__(self, cell: Cell) -> None:
        self._data = cell._checkers
        self._index = 0

    def __next__(self):
        if self._index >= len(self._data):
            raise StopIteration
        self._index += 1
        return self._data[self._index]

    def __iter__(self):
        return self

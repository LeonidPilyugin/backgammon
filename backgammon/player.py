# player.py
# Contains Player class

import threading
from typing import Tuple

from abstractplayer import AbstractPlayer
from cell import Cell
from field import Field


class Player(AbstractPlayer):
    """Player(AbstractPlayer) class
    Describes backgammon user player
    
    Methods:
        1) play(dices: Tuple[int]): plays one backgammon step
        2) mousemotion_event_handler(event: pygame.event): handles pygame.MOUSEMOTION event
        3) mousebuttondown_event_handler(event: pygame.event): handles pygame.MOUSEBUTTONDOWN event
        
    Constants:
        1) STATUS: tuple of possible statuses
    """
    STATUS = ("CHOOSE_FROM", "CHOOSE_TO", "WAIT")

    def __init__(self, field: Field):
        """Player constructor

        Args:
            field (Field): backgammon field
        """
        # set cells
        self._cells = field._cells
        # set status
        self._status = "WAIT"
        # set cell to move from
        self._from_cell = None
        # set cell to move to
        self._to_cell = None
        # list of possible steps
        self._steps = None
        # list of dices' values combinations
        self._steps_ = None
        # locker of cells
        self._cell_locker = field._cell_locker
        # locker of status
        self._status_locker = threading.Lock()
        # locker of steps
        self._steps_locker = threading.Lock()

    def play(self, dices: Tuple[int]):
        def load_steps() -> None:
            """Loads combinations of dices"""
            # one dice
            self._steps = [dices[0], dices[1]]
            # two dices
            self._steps.append(sum(self._steps))
            # save source
            self._steps_ = self._steps.copy()
            # sort
            self._steps_.sort()
            self._steps.sort()
        
        def should_pass() -> bool:
            """Returns True if should pass, else False

            Returns:
                bool: True if should pass, else False
            """
            f = False
            # for every cell check if can move from it
            for _from in self._cells:
                steps = self._steps.copy()
                if _from.index < 24 and len(_from) > 0 and _from[0].color == "red":
                    for i in range(len(steps)):
                        if self._steps[i] is not None:
                            if steps[i] > 24 - _from.index:
                                steps[i] = 24 - _from.index
                    for _to in self._cells:
                        if _to.index < 25 and _to != _from and (len(_to) == 0 or _to[0].color == "red") and \
                                _to.index - _from.index in steps:
                            f = True
                            break
                if f:
                    return False
            else:
                return True

        # load steps
        with self._steps_locker:
            load_steps()

        # move checkers
        while True:
            # pass if cannot move
            with self._steps_locker:
                if should_pass():
                    return
            
            # select cell to move from
            if self._choose_from_cell() is None:
                # if isn't chosen, restart
                continue

            # change steps if can remove cell
            with self._steps_locker:
                for i in range(len(self._steps)):
                    if self._steps[i] is not None and \
                            self._steps[i] > 24 - self._from_cell.index:
                        self._steps[i] = 24 - self._from_cell.index

            # choose cell to move to
            if self._choose_to_cell() == self._from_cell:
                # if isn't chosen, change steps to sources and restart
                with self._steps_locker:
                    for i in range(len(self._steps)):
                        if self._steps[i] is not None:
                            self._steps[i] = self._steps_.copy()[i]
                continue

            # move checker
            self._move()

            # if has steps, carry on
            with self._steps_locker:
                if self._steps.count(None) < 3:
                    continue
            # else stop
            break

    def _choose_from_cell(self) -> Cell:
        """Chooses cell to move from

        Returns:
            Cell: cell to move from
        """
        # reset from cell
        with self._cell_locker:
            self._from_cell = None
        # set status
        with self._status_locker:
            self._status = "CHOOSE_FROM"

        # wait untill from cell is chosen
        while True:
            with self._cell_locker:
                if self._from_cell is not None:
                    break

        # set status
        with self._status_locker:
            self._status = "WAIT"
        # return from cell
        return self._from_cell

    def _choose_to_cell(self) -> Cell:
        """Chooses cell to move to

        Returns:
            Cell: cell to move to
        """
        # reset to cell
        with self._cell_locker:
            self._to_cell = None
        # set status
        with self._status_locker:
            self._status = "CHOOSE_TO"

        # wait untill to cell is chosen
        while True:
            with self._cell_locker:
                if self._to_cell is not None:
                    break

        # set status
        with self._status_locker:
            self._status = "WAIT"
        # return to cell
        return self._to_cell

    def _move(self) -> None:
        """Moves checker from self._from_cell to self._to_cell and reloads steps"""
        with self._steps_locker:
            with self._cell_locker:
                # move checker
                self._from_cell.move_checker(self._to_cell)
                # get index of used step in steps
                delta = self._to_cell.index - self._from_cell.index if self._to_cell.index < 24 else \
                    24 - self._from_cell.index
                index = self._steps.index(delta)
                # there is 1 possible step, fill steps with None
                if self._steps.count(None) == 2:
                    self._steps = [None for _ in range(3)]
                else:
                    # if used step of both dices, fill steps with None
                    if index == 2:
                        self._steps = [None for _ in range(3)]
                    # else replace used step and max step with None and reload unused step
                    else:
                        self._steps = [None for _ in range(3)]
                        self._steps[1 - index] = self._steps_[1 - index]

    def mousemotion_event_handler(self, event) -> None:
        """Handles mousemotion pygame event

        Args:
            event (Event): mousemotion pygame event
        """
        with self._status_locker:
            with self._cell_locker:
                with self._steps_locker:
                    # mouse position
                    position = event.pos
                    match self._status:
                        # if choosing from, highlight possible from cells
                        case "CHOOSE_FROM":
                            for cell in self._cells:
                                if len(cell) > 0 and cell[0].color == "red" and cell.index != 24:
                                    cell.highlight("suggest")
                                    if cell.isinside(position):
                                        cell.highlight("selected")
                                        break
                        # if choosing to, highlight possible to cells
                        case "CHOOSE_TO":
                            for cell in self._cells:
                                if cell.index != 25 and cell.index - self._from_cell.index in self._steps and \
                                        cell != self._from_cell and \
                                        (len(cell) == 0 or cell[0].color != "black"):
                                    cell.highlight("suggest")
                                    if cell.isinside(position):
                                        cell.highlight("hover")
                                        break

    def mousebuttondown_event_handler(self, event) -> None:
        """Handles mousebuttondown pygame event

        Args:
            event (Event): mousebuttondown pygame event
        """
        with self._status_locker:
            with self._cell_locker:
                # mouse position
                position = event.pos
                match self._status:
                    # if choosing from, set from cell
                    case "CHOOSE_FROM":
                        for cell in self._cells:
                            if len(cell) > 0 and cell[0].color == "red" and cell.index < 24:
                                cell.highlight("suggest")
                                if cell.isinside(position):
                                    for c in self._cells:
                                        c.highlight(None)
                                    cell.highlight("selected")
                                    self._status = "WAIT"
                                    self._from_cell = cell
                                    break
                    # if choosing to, set to cell
                    case "CHOOSE_TO":
                        for cell in self._cells:
                            if cell.isinside(position) and \
                                    (cell.color == Cell.COLORS["hover"] or cell.color == Cell.COLORS["selected"]):
                                self._to_cell = cell
                                cell.highlight(None)
                                self._status = "WAIT"
                                for cell in self._cells:
                                    cell.highlight(None)
                                break

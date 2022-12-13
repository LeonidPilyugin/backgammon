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
        1) play(dices: Tuple[int, int]): plays one backgammon step
        2) mousemotion_event_handler(position: Tuple[int, int]): handles pygame.MOUSEMOTION event
        3) mousebuttondown_event_handler(position: Tuple[int, int]): handles pygame.MOUSEBUTTONDOWN event
        4) move_mouse(position: Tuple[int, int]): moves mouse pointer
        
    Constants:
        1) STATUS: tuple of possible statuses
    """
    
    STATUS = ("CHOOSE_FROM", "CHOOSE_TO", "WAIT")  # tuple of possible statuses

    def __init__(self, field: Field):
        """Player constructor

        Args:
            field (Field): backgammon field
        """
        
        self._cells = field._cells  # set cells
        self._status = "WAIT"  # set status
        
        self._from_cell = None  # set cell to move from
        self._to_cell = None  # set cell to move to
        
        self._steps = None  # list of possible steps
        self._steps_ = None  # list of dices' values combinations
        
        self._mouse_pos = (0, 0)  # mouse position
        
        self._cell_locker = field._cell_locker  # locker of cells
        self._status_locker = threading.Lock()  # locker of status
        self._steps_locker = threading.Lock()  # locker of steps
        self._mouse_pos_locker = threading.Lock()  # locker of mouse position

    def move_mouse(self, position: Tuple[int, int]) -> None:
        """Sets mouse position

        Args:
            position (Tuple[int, int]): mouse position
        """
        
        with self._mouse_pos_locker:  # lock mouse position
            self._mouse_pos = position  # set position

    def play(self, dices: Tuple[int]):
        
        def load_steps() -> None:
            """Loads combinations of dices"""
            
            self._steps = [dices[0], dices[1]]  # one dice used step
            self._steps.append(sum(self._steps))  # two dice used step
            self._steps_ = self._steps.copy()  # save source
            self._steps_.sort()  # sort _steps_
            self._steps.sort()  # sort _steps

        def should_pass() -> bool:
            """Returns True if should pass, else False

            Returns:
                bool: True if should pass, else False
            """
            
            f = False  # flag to return if should not pass
            
            for _from in self._cells:  # for every cell check if can move from it
                steps = self._steps.copy()  # copy possible steps
                
                if _from.index < 24 and len(_from) > 0 \
                    and _from[0].color == "red":  # if can move from this cell
                    
                    for i in range(len(steps)):  # if too close to final cell, change steps
                        if self._steps[i] is not None:
                            if steps[i] > 24 - _from.index:
                                steps[i] = 24 - _from.index
                                
                    for _to in self._cells:  # check if can move to ofher cells
                        if _to.index < 25 and _to != _from and \
                            (len(_to) == 0 or _to[0].color == "red") and \
                                _to.index - _from.index in steps: # can move to cell _to
                            f = True
                            break
                        
                if f:  # shouldn't pass
                    return False
            else:      # should pass
                return True

        with self._steps_locker:  # lock steps
            load_steps()  # load steps

        while True:  # play while can move
            with self._steps_locker:  # lock steps
                if should_pass():  # return if cannot move
                    return

            with self._mouse_pos_locker:  # lock mouse position
                with self._status_locker:  # lock status
                    self._status = "CHOOSE_FROM"  # choose status
                self.mousemotion_event_handler(self._mouse_pos)  # highlight cells

            if self._choose_from_cell() is None:  # select cell to move from
                continue  # if cell isn't chosen, choose again

            with self._steps_locker:  # lock steps
                for i in range(len(self._steps)):  # change steps if can remove cell
                    if self._steps[i] is not None and \
                            self._steps[i] > 24 - self._from_cell.index:
                        self._steps[i] = 24 - self._from_cell.index

            with self._mouse_pos_locker:  # lock mouse position
                with self._status_locker:  # lock status
                    self._status = "CHOOSE_TO"  # choose status
                self.mousemotion_event_handler(self._mouse_pos)  # highlight cells

            if self._choose_to_cell() == self._from_cell:  # to cell isn't chosen
                with self._steps_locker:  # lock steps
                    for i in range(len(self._steps)):  # recover steps
                        if self._steps[i] is not None:
                            self._steps[i] = self._steps_.copy()[i]
                continue  # choose cells again

            self._move()  # move checker

            with self._steps_locker:  # lock steps
                if self._steps.count(None) < 3:  # if has steps, move again
                    continue
            
            break  # else return

    def _choose_from_cell(self) -> Cell:
        """Chooses cell to move from

        Returns:
            Cell: cell to move from
        """
        
        with self._cell_locker:  # lock cells
            self._from_cell = None  # reset from cell
        
        with self._status_locker:  # lock status
            self._status = "CHOOSE_FROM"  # set status

        # wait untill from cell is chosen
        while True:
            with self._cell_locker:
                if self._from_cell is not None:
                    break

        with self._status_locker:  # lock status
            self._status = "WAIT"  # set status
        
        return self._from_cell  # return from cell

    def _choose_to_cell(self) -> Cell:
        """Chooses cell to move to

        Returns:
            Cell: cell to move to
        """
        
        with self._cell_locker:  # lock cells
            self._to_cell = None  # reset to cell
        
        with self._status_locker:  # lock status
            self._status = "CHOOSE_TO"  # set status

        # wait untill to cell is chosen
        while True:
            with self._cell_locker:
                if self._to_cell is not None:
                    break

        with self._status_locker:  # lock status
            self._status = "WAIT"  # set status
        
        return self._to_cell  # return to cell

    def _move(self) -> None:
        """Moves checker from self._from_cell to self._to_cell and reloads steps"""
        
        with self._steps_locker:  # lock steps
            with self._cell_locker:  # lock cell
                self._from_cell.move_checker(self._to_cell)  # move checker
                    
                delta = self._to_cell.index - self._from_cell.index if \
                    self._to_cell.index < 24 else 24 - self._from_cell.index  # size of used step
                index = self._steps.index(delta)  # index of this step in steps
                
                if self._steps.count(None) == 2:  # if there is one step in steps
                    self._steps = [None for _ in range(3)]  # clear steps
                else:  # if more than one step
                    if index == 2:  # if used step of both dices
                        self._steps = [None for _ in range(3)]  # clear steps
                    else:  # if used step of one dice
                        self._steps = [None for _ in range(3)]  # clear steps
                        self._steps[1 - index] = self._steps_[1 - index]  # recover unused steps

    def _highlight_mousemotion_from(self, position: Tuple[int, int]) -> None:
        """Highlights cells if status is "CHOOSE_FROM" and event is MOUSEMOTION

        Args:
            position (Tuple[int, int]): mouse position
        """
        
        for cell in self._cells:
            if len(cell) > 0 and cell[0].color == "red"\
                    and cell.index != 24:  # if can move from this cell
                cell.highlight("suggest")  # highlight cell as suggested
                
                if cell.isinside(position):  # if is inside cell
                    cell.highlight("selected")  # highlight cell as selected

    def _highlight_mousemotion_to(self, position: Tuple[int, int]) -> None:
        """Highlights cells if status is "CHOOSE_TO" and event is MOUSEMOTION

        Args:
            position (Tuple[int, int]): mouse position
        """
        
        for cell in self._cells:
            if cell.index != 25 and cell.index - self._from_cell.index in self._steps and \
                    cell != self._from_cell and \
                    (len(cell) == 0 or cell[0].color != "black"): # if can move to cell
                cell.highlight("suggest")  # highlight cell as suggested
                
                if cell.isinside(position):  # if is inside cell
                    cell.highlight("hover")  # highlight cell as hovered

    def _highlight_mousebuttondown_from(self, position: Tuple[int, int]) -> None:
        """Highlights cells if status is "CHOOSE_FROM" and event is MOUSENUTTONDOWN

        Args:
            position (Tuple[int, int]): mouse position
        """
        
        for cell in self._cells:
            if len(cell) > 0 and cell[0].color == "red"\
                    and cell.index < 24:  # if can move from cell
                cell.highlight("suggest")  # highlight cell as suggested
                
                if cell.isinside(position):  # if is inside
                    for c in self._cells:  # reset highlight of all cells
                        c.highlight(None)
                        
                    cell.highlight("selected")  # highlight cell as selected
                    self._status = "WAIT"  # change status
                    self._from_cell = cell  # set from cell
                    
                    break

    def _highlight_mousebuttondown_to(self, position: Tuple[int, int]) -> None:
        """Highlights cells if status is "CHOOSE_TO" and event is MOUSEBUTTONDOWN

        Args:
            position (Tuple[int, int]): mouse position
        """
        
        for cell in self._cells:
            if cell.isinside(position) and \
                    (cell.color == Cell.COLORS["hover"] or \
                        cell.color == Cell.COLORS["selected"]):  # if can move to cell
                self._to_cell = cell  # set to vell
                self._status = "WAIT"  # set status
                
                for c in self._cells:  # reset cells highlight
                    c.highlight(None)
                    
                break

    def mousemotion_event_handler(self, position: Tuple[int, int]) -> None:
        """Handles mousemotion pygame event

        Args:
            position (Tuple[int, int]): mouseposition
        """
        
        with self._status_locker:  # lock status
            with self._cell_locker:  # lock cell
                with self._steps_locker:  # lock steps
                    match self._status:  # match status
                        case "CHOOSE_FROM":  # choosing from cell
                            self._highlight_mousemotion_from(position)  # highlight
                        case "CHOOSE_TO":  # choosing to cell
                            self._highlight_mousemotion_to(position)  # highlight

    def mousebuttondown_event_handler(self, position: Tuple[int, int]) -> None:
        """Handles mousebuttondown pygame event

        Args:
            position (Tuple[int, int]): mouseposition
        """
        with self._status_locker:  # lock status
            with self._cell_locker:  # lock cell
                match self._status:  # match status
                    case "CHOOSE_FROM":  # choosing from cell
                        self._highlight_mousebuttondown_from(position)  # highlight
                    case "CHOOSE_TO":  # choosing to cell
                        self._highlight_mousebuttondown_to(position)  # highlight

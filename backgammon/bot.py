import threading
from typing import Tuple

import pygame

from abstractplayer import AbstractPlayer
from cell import Cell
from field import Field


class Bot(AbstractPlayer):
    STATUS = ("CHOOSE_FROM", "CHOOSE_TO", "WAIT")

    def __init__(self, field: Field):
        self._cells = field._cells
        self._status = "WAIT"
        self._from_cell = None
        self._to_cell = None
        self._steps = None
        self._steps_ = None
        self._cell_locker = field._cell_locker
        self._status_locker = threading.Lock()
        self._steps_locker = threading.Lock()

    def play(self, dices: Tuple[int]):
        def load_steps():
            self._steps = [dices[0], dices[1]]
            self._steps.append(sum(self._steps))
            self._steps_ = self._steps.copy()
            self._steps_.sort()
            self._steps.sort()
            
        def should_pass() -> bool:
            f = False
            for _from in self._cells:
                steps = self._steps.copy()
                if _from.index < 24 and len(_from) > 0 and _from[0].color == "black":
                    for i in range(len(steps)):
                        if self._steps[i] is not None:
                            if steps[i] > 24 - Bot._conv_index(_from.index):
                                steps[i] = 24 - Bot._conv_index(_from.index)
                    for _to in self._cells:
                        if Bot._conv_index(_to.index) < 25 and _to != _from and (len(_to) == 0 or _to[0].color == "black") and \
                                Bot._conv_index(_to.index) - Bot._conv_index(_from.index) in steps:
                            f = True
                            break
                if f:
                    return False
            else:
                return True

        with self._steps_locker:
            load_steps()
            if should_pass():
                return

        # SUS MOMENT
        while True:
            with self._steps_locker:
                if should_pass():
                    return
            
            if self._choose_from_cell() is None:
                continue

            with self._steps_locker:
                for i in range(len(self._steps)):
                    if self._steps[i] is not None and \
                            self._steps[i] > 24 - Bot._conv_index(self._from_cell.index):
                        self._steps[i] = 24 - Bot._conv_index(self._from_cell.index)

            if self._choose_to_cell() is None:
                with self._steps_locker:
                    for i in range(len(self._steps)):
                        if self._steps[i] is not None:
                            self._steps[i] = self._steps_.copy()[i]
                continue

            self._move()

            with self._steps_locker:
                if self._steps.count(None) < 3:
                    continue
            break

    def _conv_index(index: int) -> int:
        return 24 if index == 25 else 25 if index == 24 else 12 + index if index < 12 else index - 12

    def _choose_from_cell(self) -> Cell:
        with self._cell_locker:
            self._from_cell = None

        with self._status_locker:
            self._status = "CHOOSE_FROM"

        while True:
            with self._cell_locker:
                if self._from_cell is not None:
                    break

        with self._status_locker:
            self._status = "WAIT"
        return self._from_cell

    def _choose_to_cell(self) -> Cell:
        with self._cell_locker:
            self._to_cell = None

        with self._status_locker:
            self._status = "CHOOSE_TO"

        while True:
            with self._cell_locker:
                if self._to_cell is not None:
                    if self._to_cell == self._from_cell:
                        with self._status_locker:
                            self._status = "WAIT"
                        return None
                    break

        with self._status_locker:
            self._status = "WAIT"

        return self._to_cell

    # SUS MOMENT
    def _move(self):
        with self._steps_locker:
            with self._cell_locker:
                self._from_cell.move_checker(self._to_cell)

                delta = Bot._conv_index(self._to_cell.index) - \
                        Bot._conv_index(self._from_cell.index) if self._to_cell.index < 24 else \
                    12 - self._from_cell.index
                index = self._steps.index(delta)
                if self._steps.count(None) == 2:
                    self._steps = [None for _ in range(3)]
                else:
                    if index == 2:
                        self._steps = [None for _ in range(3)]
                    else:
                        self._steps = [None for _ in range(3)]
                        self._steps[1 - index] = self._steps_[1 - index]

    def mousemotion_event_handler(self, event: pygame.event) -> None:
        with self._status_locker:
            with self._cell_locker:
                with self._steps_locker:
                    position = event.pos
                    match self._status:
                        case "CHOOSE_FROM":
                            for cell in self._cells:
                                if len(cell) > 0 and cell[0].color == "black" and cell.index != 25:
                                    cell.highlight("suggest")
                                    if cell.isinside(position):
                                        for c in self._cells:
                                            c.highlight(None)
                                        cell.highlight("selected")
                                        break

                        case "CHOOSE_TO":
                            for cell in self._cells:
                                if cell.index != 24 and Bot._conv_index(cell.index) - \
                                        Bot._conv_index(self._from_cell.index) in self._steps and \
                                        cell != self._from_cell and \
                                        (len(cell) == 0 or cell[0].color != "red"):
                                    cell.highlight("suggest")
                                    if cell.isinside(position):
                                        cell.highlight("hover")
                                        break

    def mousebuttondown_event_handler(self, event: pygame.event) -> None:
        with self._status_locker:
            with self._cell_locker:
                position = event.pos
                match self._status:
                    case "CHOOSE_FROM":
                        for cell in self._cells:
                            if len(cell) > 0 and cell[0].color == "black" and cell.index < 24:
                                cell.highlight("suggest")
                                if cell.isinside(position):
                                    for c in self._cells:
                                        c.highlight(None)
                                    cell.highlight("selected")
                                    self._status = "WAIT"
                                    self._from_cell = cell
                                    break

                    case "CHOOSE_TO":
                        for cell in self._cells:
                            if cell.isinside(position) and \
                                    (cell.color == Cell.COLORS["hover"] or cell.color == Cell.COLORS["selected"]):
                                self._to_cell = cell
                                cell.highlight(None)
                                for cell in self._cells:
                                    cell.highlight(None)
                                break

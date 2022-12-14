from typing import Tuple

from abstractplayer import AbstractPlayer
from field import Field


class Bot(AbstractPlayer):
    def __init__(self, field: Field) -> None:
        """Smartbot constructor
                Args:
                    field (Field): backgammon field
                """
        # set cells
        self._cells = field._cells
        # list of possible steps
        self._steps = None
        # list of dices' values combinations
        self._steps_ = None

    def play(self, dices: Tuple[int]) -> None:
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

        load_steps()
        while self._steps.count(0) != 3 and should_pass() is False:
            self.move_checkers()

    def move_checkers(self):
        for i in range(24):
            if self._is_possible(i):
                continue
            elif Bot._conv_index(i) + self._steps[2] >= 24:
                self._cells[i].move_checker(self._cells[25])
                self._steps[2] = 0
                if 24 - Bot._conv_index(i) > self._steps[1]:
                    self._steps[0] = 0
                    self._steps[1] = 0
                elif 24 - Bot._conv_index(i) > self._steps[0]:
                    self._steps[1] = 0
                else:
                    self._steps[0] = 0
        for i in range(24):
            if self._is_possible(i):
                continue
            elif len(self._cells[i]._checkers) >= 2 and \
                    self._is_possible_move(Bot._conv_index(Bot._conv_index(i) + self._steps[0])) is False:
                self._cells[i].move_checker(self._cells[Bot._conv_index(Bot._conv_index(i) + self._steps[0])])
                self._steps[0] = 0
                self._steps[2] = 0
        for i in range(24):
            if self._is_possible(i):
                continue
            elif len(self._cells[i]._checkers) >= 2 and \
                    self._is_possible_move(Bot._conv_index(Bot._conv_index(i) + self._steps[1])) is False:
                self._cells[i].move_checker(self._cells[Bot._conv_index(Bot._conv_index(i) + self._steps[1])])
                self._steps[1] = 0
                self._steps[2] = 0
        for i in range(24):
            if self._is_possible(i):
                continue
            elif len(self._cells[i]._checkers) >= 2 and \
                    self._is_possible_move(Bot._conv_index(Bot._conv_index(i) + self._steps[2])) is False:
                self._cells[i].move_checker(self._cells[Bot._conv_index(Bot._conv_index(i) + self._steps[2])])
                self._steps[0] = 0
                self._steps[1] = 0
                self._steps[2] = 0
        for i in range(24):
            if self._is_possible(i):
                continue
            elif len(self._cells[i]._checkers) == 1 and \
                    self._is_possible_move(Bot._conv_index(Bot._conv_index(i) + self._steps[0])) is False:
                self._cells[i].move_checker(self._cells[Bot._conv_index(Bot._conv_index(i) + self._steps[0])])
                self._steps[0] = 0
                self._steps[2] = 0
        for i in range(24):
            if self._is_possible(i):
                continue
            elif len(self._cells[i]._checkers) == 1 and \
                    self._is_possible_move(Bot._conv_index(Bot._conv_index(i) + self._steps[1])) is False:
                self._cells[i].move_checker(self._cells[Bot._conv_index(Bot._conv_index(i) + self._steps[1])])
                self._steps[1] = 0
                self._steps[2] = 0
        for i in range(24):
            if self._is_possible(i):
                continue
            elif len(self._cells[i]._checkers) == 1 and \
                    self._is_possible_move(Bot._conv_index(Bot._conv_index(i) + self._steps[2])) is False:
                self._cells[i].move_checker(self._cells[Bot._conv_index(Bot._conv_index(i) + self._steps[2])])
                self._steps[0] = 0
                self._steps[1] = 0
                self._steps[2] = 0

    def _is_possible(self, cell_number):
        return True if (len(self._cells[cell_number]._checkers) != 0
                        and self._cells[cell_number]._checkers[0]._color == "red") \
                       or len(self._cells[cell_number]._checkers) == 0 else False

    def _is_possible_move(self, cell_number):
        return True if len(self._cells[cell_number]._checkers) != 0 \
                       and self._cells[cell_number]._checkers[0]._color == "red" else False

    def _conv_index(index: int) -> int:
        return 24 if index == 25 else 25 if index == 24 else 12 + index if index < 12 else index - 12
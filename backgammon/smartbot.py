from typing import Tuple
from field import Field
from abstractplayer import AbstractPlayer
from cell import Cell

class Bot(AbstractPlayer):
    def __init__(self, field: Field) -> None:
        pass
    
    def play(self, dices: Tuple[int]) -> None:
        pass
    
    def _conv_index(index: int) -> int:
        return 24 if index == 25 else 25 if index == 24 else 12 + index if index < 12 else index - 12
    
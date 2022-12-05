# abstractplayer.py
# Contains AbstractPlayer abstract class

from abc import ABCMeta, abstractmethod
from typing import Tuple


class AbstractPlayer(metaclass=ABCMeta):
    """AbstractPlayer class
    Describes backgammon player
    
    Methods:
        1) play(dices: Tuple[int]): plays one backgammon step
    """

    @abstractmethod
    def play(self, dices: Tuple[int, int]) -> None:
        """Plays one backgammon step

        Args:
            dices (Tuple[int]): tuple of dices' values (length is 2)
        """
        pass

from enum import Enum


class BetRules(Enum):
    NATURAL_BLACK_JACK = 2.5
    WIN = 2
    DRAW = 1
    LOSE = -1

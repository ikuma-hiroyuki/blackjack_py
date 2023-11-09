from dataclasses import dataclass


@dataclass
class BetRules:
    NATURAL_BLACK_JACK = 2.5
    WIN = 2
    DRAW = 1
    LOSE = 0

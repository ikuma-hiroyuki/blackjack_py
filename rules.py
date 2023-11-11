from enum import Enum


class ScoreRules(Enum):
    """スコア計算に関するルールを表す列挙型"""
    BLACK_JACK_VALUE = 21
    DEALER_MIN_VALUE = 17


class Odds(Enum):
    """掛け金分配率を表す列挙型"""
    NATURAL_BLACK_JACK = 2.5
    WIN = 2
    DRAW = 1
    LOSE = -1

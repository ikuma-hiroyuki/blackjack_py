import colorama
from art_manager import ArtManager

BLACK_JACK_VALUE = 21
DEALER_MIN_VALUE = 17


class Card:
    """カード一枚一枚を表すクラス"""
    art_manager = ArtManager()

    SUITS = {
        '♣': colorama.Fore.RESET,
        '♥': colorama.Fore.RED,
        '♠': colorama.Fore.RESET,
        '♦': colorama.Fore.RED
    }

    CARD_SCORE = {
        'A': {'score': 11, 'is_ace': True},
        '2': {'score': 2},
        '3': {'score': 3},
        '4': {'score': 4},
        '5': {'score': 5},
        '6': {'score': 6},
        '7': {'score': 7},
        '8': {'score': 8},
        '9': {'score': 9},
        '10': {'score': 10},
        'J': {'score': 10},
        'Q': {'score': 10},
        'K': {'score': 10},
    }

    def __init__(self, suit, rank):
        self.suit = self._set_color(suit, suit)  # スート(♠, ♣, ♥, ♦)のこと
        self.rank = self._set_color(suit, rank)  # 絵柄(A, 2, 3, ..., 10, J, Q, K)のこと
        self.score = self.CARD_SCORE[rank]['score']  # ランクの得点
        self.is_ace = self.CARD_SCORE[rank].get('is_ace', False)  # A かどうか

    @classmethod
    def _set_color(cls, suit, value):
        return f"{cls.SUITS[suit]}{value}" + colorama.Fore.RESET

    def _create_card_ascii_art(self):
        """
        カードのアスキーアートを生成して返す
        :return: カードのアスキーアート
        """
        return self.art_manager.card_face.format(self.rank.ljust(12, " "), self.suit, self.rank.rjust(12, "_"))

    def get_card_art(self, show_face=True):
        """
        カードのアスキーアートを返す
        :param show_face: True: 表向き, False: 裏向き
        :return: カードのアスキーアート
        """
        return self._create_card_ascii_art() if show_face else self.art_manager.card_back

    def __repr__(self):
        return f'{self.suit}{self.rank}'

import colorama

from art_manager import art_manager

BLACK_JACK_VALUE = 21


class Card:
    """カード一枚一枚を表すクラス"""

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
        return art_manager.card_face.format(self.rank.ljust(12, " "), self.suit, self.rank.rjust(12, "_"))

    def show_card(self, show_face=True, show_score=False):
        """
        カードのアスキーアートを表示する
        :param show_face: カードの表を見せるか
        :param show_score: カードの得点を表示するか
        """

        card_aa = self._create_card_ascii_art() if show_face else art_manager.card_back
        if show_score:
            score = f'{self.score}' if not self.is_ace else f'{self.score} or {self.score - 10}'
            print(f'{card_aa} {score}点')
        else:
            print(card_aa)

    def __repr__(self):
        return f'{self.suit}{self.rank}'

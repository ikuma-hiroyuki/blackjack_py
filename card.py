import colorama
from art_manager import art_manager

colorama.init(autoreset=True)


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

    def __init__(self, suit, rank, score):
        self.suit = suit  # スート(♠, ♣, ♥, ♦)のこと
        self.rank = rank  # 絵柄(A, 2, 3, ..., 10, J, Q, K)のこと
        self.score = score['score']  # ランクの得点
        self.is_ace = score.get('is_ace', False)  # A かどうか

    def _create_card_ascii_art(self):
        """
        カードのアスキーアートを生成して返す
        :return: カードのアスキーアート
        """

        colored_suit = f"{self.SUITS[self.suit]}{self.suit}" + colorama.Fore.RESET
        return art_manager.card_face.format(self.rank.ljust(2, " "), colored_suit, self.rank.rjust(2, "_"))

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
        return f'{self.SUITS[self.suit]}{self.suit}{self.rank}'


if __name__ == '__main__':
    club_ace = Card('♣', 'A', {'score': 11, 'is_ace': True})
    print(club_ace)
    club_ace.show_card()

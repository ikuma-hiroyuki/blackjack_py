from art_manager import art_manager


class Card:
    """カード一枚一枚を表すクラス"""

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

        return art_manager.card_face.format(self.rank.ljust(2, " "), self.suit, self.rank.rjust(2, "_"))

    def show_card(self, show_face=True, show_score=False):
        """
        カードのアスキーアートを表示する
        :param show_face: カードの表を見せるか
        :param show_score: カードの得点を表示するか
        """

        card_aa = self._create_card_ascii_art() if show_face else art_manager.card_back
        if show_score:
            score = f'{self.score}' if not self.is_ace else f'{self.score} or {self.score - 10}'
            card_aa += f' {score}点'
        print(card_aa)

    def __repr__(self):
        return f'{self.suit}{self.rank}'

import random

from card import Card, BLACK_JACK_VALUE
from deck import Deck


class Player:
    # プレイヤー間で共通して使うデッキ
    deck = Deck()

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.is_stand = False
        self.is_bust = False
        self.hand: list[Card] = []

    def hit(self):
        """カードを1枚引いてスコアを計算する"""

        random_index = random.randint(0, len(self.deck.card_list) - 1)
        self.hand.append(self.deck.card_list.pop(random_index))
        self._calculate_score()
        if self.score > BLACK_JACK_VALUE:
            self.is_bust = True

    def stand(self):
        """スタンドしてスコアを計算する"""

        self.is_stand = True
        self._calculate_score()

    def _calculate_score(self):
        """手札のスコアを計算する"""

        initial_score = sum(card.score for card in self.hand)
        ace_count = sum(1 for card in self.hand if card.is_ace)

        adjusted_score = initial_score
        while adjusted_score > BLACK_JACK_VALUE and ace_count > 0:
            adjusted_score -= 10
            ace_count -= 1
        self.score = adjusted_score

    def show_all_card_face(self):
        """複数のカードを横一列で表示する"""

        line1_list = []
        line2_list = []
        line3_list = []
        line4_list = []

        for card in self.hand:
            line1, line2, line3, line4 = card.get_card_art().splitlines()
            line1_list.append(line1.ljust(5, " "))
            line2_list.append(line2.ljust(5, " "))
            line3_list.append(line3.ljust(5, " "))
            line4_list.append(line4.ljust(5, " "))

        print("  ".join(line1_list))
        print("  ".join(line2_list))
        print("  ".join(line3_list))
        print("  ".join(line4_list))
        print(f'スコア: {self.score}点')

    def reset_game(self):
        """ゲームをリセット"""

        self.deck = Deck()
        self.score = 0
        self.is_stand = False
        self.is_bust = False
        self.hand = []


class User(Player):
    def __init__(self):
        super().__init__('ユーザー')
        self.money = 0


if __name__ == '__main__':
    user = User()
    user.hit()
    user.hit()
    user.show_all_card_face()

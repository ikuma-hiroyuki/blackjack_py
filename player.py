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

    def show_card_face(self, num_visible_cards):
        """
        指定された数のカードの表を表示する

        残りのカードは裏を表示する
        :param num_visible_cards: 表向きにするカードの枚数
        """

        lines = [""] * 4  # カードのAAを表示するための4行分のスペースを用意

        for i, card in enumerate(self.hand):
            # カードのAAを1行ごとに分割してリストにする
            lines_of_card = card.get_card_art(show_face=i < num_visible_cards).splitlines()
            # 各行のカードのAAをスペースで区切って連結する
            for j, line in enumerate(lines_of_card):
                lines[j] += line.ljust(5) + " "

        print("\n".join(lines))

    def show_all_card_face(self):
        """全てのカードの表を表示する"""
        self.show_card_face(num_visible_cards=len(self.hand))

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

    dealer = Player('ディーラー')
    dealer.hit()
    dealer.hit()
    dealer.hit()
    dealer.show_card_face(num_visible_cards=1)

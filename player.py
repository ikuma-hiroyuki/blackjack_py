from enum import Enum, auto

from card import Card, Deck
from deal_helper import ScoreRules


class Player:
    """プレイヤーを表すクラス"""

    # プレイヤー間で共通して使うデッキ
    deck = Deck()

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.is_stand = False
        self.is_burst = False
        self.hand: list[Card] = []

    def hit(self, *args):
        """カードを1枚引いてスコアを計算する"""

        self.hand.append(self.deck.deal_a_card())
        self.calculate_score()
        if self.score > ScoreRules.BLACK_JACK.value:
            self.is_burst = True

    def stand(self):
        """スタンドしてスコアを計算する"""

        self.is_stand = True
        self.calculate_score()

    def calculate_score(self):
        """手札のスコアを計算する"""

        initial_score = sum(card.score for card in self.hand)
        ace_count = sum(1 for card in self.hand if card.is_ace)

        adjusted_score = initial_score
        while adjusted_score > ScoreRules.BLACK_JACK.value and ace_count > 0:
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

    def show_all_face_and_score(self):
        """全てのカードの表を表示する"""
        self.show_card_face(num_visible_cards=len(self.hand))
        print(f"{self.name}のスコア: {self.score}")

    def reset_deal(self):
        """リセットして次の勝負に備える"""
        self.score = 0
        self.is_stand = False
        self.is_burst = False
        self.hand = []


class User(Player):
    def __init__(self):
        super().__init__('ユーザー')
        self._money = 1000
        self.game_result = UserGameStateEnum.INIT
        self.bet_amount = 0
        self.bet_distribute_rate = 0
        self.is_natural_blackjack = False

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, value):
        self._money = int(value)

    @property
    def bet_result_amount(self):
        """勝負の結果得た(失った)金額を返す"""
        return int(self.bet_amount * self.bet_distribute_rate)

    def reset_deal(self):
        """リセットして次の勝負に備える"""
        super().reset_deal()
        self.game_result = UserGameStateEnum.INIT
        self.bet_amount = 0
        self.bet_distribute_rate = 0
        self.is_natural_blackjack = False


class Dealer(Player):
    def __init__(self):
        super().__init__('ディーラー')

    def reset_deal(self):
        """リセットして次の勝負に備えるとともに、デッキをリセットする"""
        super().reset_deal()
        Player.deck = Deck()


class UserGameStateEnum(Enum):
    """ユーザーの勝敗結果状態を表す列挙型"""
    INIT = auto()
    WIN = auto()
    DRAW = auto()
    LOSE = auto()

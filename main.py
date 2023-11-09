from enum import Enum, auto

from art_manager import ArtManager
from player import User, Dealer, Player
from rules.bet_rules import BetRules
from rules.score_rules import ScoreRules


class UserGameState(Enum):
    """ユーザーの勝敗結果状態を表す列挙型"""
    INIT = auto()
    WIN = auto()
    DRAW = auto()
    LOSE = auto()


class UserState:
    """ユーザーの状態を管理するクラス"""

    def __init__(self):
        self.game_result = UserGameState.INIT
        self.bet_amount = 0
        self.bet_distribute_rate = 0
        self.is_natural_blackjack = False


class GameManager:
    """ブラックジャックのゲームを管理するクラス"""
    art = ArtManager()

    def __init__(self):
        self.user = User()
        self.user_state = UserState()
        self.dealer = Dealer()
        self.players = [self.user, self.dealer]  # ユーザー、ディーラーの順番でカードを配る

    def play_game(self):
        """ゲームを開始する"""
        self._play_rounds()

    def _play_rounds(self):
        """各ラウンドをプレイする"""
        while True:
            self._round_of_game()
            if not self._is_user_replay_decision():
                break

            self._reset_game()

    def _round_of_game(self):
        """ゲームを1回戦行う"""

        self._ask_bets()
        self._deal_card()
        self._show_initial_hands()

        for player in self.players:
            self._round_for_stand_or_burst(player)
            self._check_natural_blackjack(player)

        self._evaluate_judge()
        self._distribute_bets()

    def _deal_card(self):
        """ゲーム開始直後にユーザーとディーラーインスタンスに2枚ずつカードを配る"""
        for _ in range(2):
            for player in self.players:
                player.hit()

    def _round_for_stand_or_burst(self, player: Player):
        """
        プレイヤーがスタンドもしくはバーストするまで待機する(繰り返す)
        :param player: ユーザーもしくはディーラーインスタンス
        """
        while player.is_stand or player.is_burst:
            player.hit()

            if isinstance(player, User):
                self._show_initial_hands()

            if isinstance(player, Dealer):
                self._show_final_hands()

            self.show_burst_status(player)

    def _show_initial_hands(self):
        """ユーザーの全てのカードを表に、ディーラーの1枚のカードを表にする"""

    def _show_final_hands(self):
        """ユーザーとディーラーの全てのカードを表にする"""

    def show_burst_status(self, player: Player):
        """
        バーストしていればAAを表示する
        :param player: ユーザーもしくはディーラーインスタンス
        """

        if player.is_burst:
            print(f"{player.name}: バースト")
            print(self.art.burst)

    def _check_natural_blackjack(self, player: Player):
        """
        ナチュラルブラックジャックかどうか判定し、ユーザーがそうだった場合はAAを表示する
        :param player: ユーザーもしくはディーラーインスタンス
        """

        result = player.score == ScoreRules.BLACK_JACK_VALUE and len(player.hand) == 2
        if isinstance(player, User):
            print(f"{player.name}: ブラックジャック！")
            print(self.art.blackjack)
            self.user_is_natural_blackjack = result

    def _evaluate_judge(self):
        """ユーザーの勝敗を判定し掛け金分配率を決定する"""
        self.user_state.game_result = self._judge_game_state()
        self.user_state.bet_distribute_rate = self._judge_distribute_bet()

    def _judge_game_state(self):
        """ユーザーの勝敗を判定する"""
        if self.user.is_burst:
            return UserGameState.LOSE
        if self.dealer.is_burst:
            return UserGameState.WIN

        if self.user.score > self.dealer.score:
            return UserGameState.WIN
        elif self.user.score == self.dealer.score:
            return UserGameState.DRAW
        else:
            return UserGameState.LOSE

    def _judge_distribute_bet(self):
        """掛け金分配率を決定する"""
        if self.user_state.game_result == UserGameState.WIN:
            return BetRules.NATURAL_BLACK_JACK.value if self.user_is_natural_blackjack else BetRules.WIN.value
        elif self.user_state.game_result == UserGameState.DRAW:
            return BetRules.DRAW.value
        else:
            return BetRules.LOSE.value

    @staticmethod
    def _is_user_replay_decision():
        """ユーザーに再戦するかどうか尋ねる"""
        return bool(input('再戦する場合は何か入力してエンターキーを押してください: '))

    def _ask_bets(self):
        """掛け金をユーザーに尋ねる"""

    def _distribute_bets(self):
        """掛け金を分配する"""
        self.user.money += self.user_state.bet_amount * self.user_state.bet_distribute_rate

    def _reset_game(self):
        """ゲームをリセットする"""
        for player in self.players:
            player.reset_deal()
        self.user_state = UserState()


if __name__ == '__main__':
    game_manager = GameManager()
    game_manager.play_game()

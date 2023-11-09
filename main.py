from art_manager import ArtManager
from player import User, Dealer, Player
from rules.score_rules import ScoreRules


class GameManager:
    """ブラックジャックのゲームを管理するクラス"""
    art = ArtManager()

    def __init__(self):
        self.user = User()
        self.dealer = Dealer()
        self.players = [self.user, self.dealer]  # ユーザー、ディーラーの順番でカードを配り、ヒットかスタンドを尋ねる

    def play_game(self):
        """ゲームを開始する"""
        self._play_rounds()

    def _play_rounds(self):
        """各ラウンドをプレイする"""
        while True:
            self._round_of_game()
            if not self._is_user_replay_decision():
                break

            for player in self.players:
                player.reset_deal()

    def _round_of_game(self):
        """ゲームを1回戦行う"""
        self._ask_bets()
        self._deal_card()
        self._show_initial_hands()

        for player in self.players:
            self._round_for_stand_or_burst(player)

            if player.is_burst:
                print(f"{player.name}: バースト")
                print(self.art.burst)
                break

            if player.score == ScoreRules.BLACK_JACK_VALUE and len(player.hand) == 2:
                print(f"{player.name}: ブラックジャック！")
                print(self.art.blackjack)

        self._evaluate_judge()
        self._distribute_bets()

    def _deal_card(self):
        """ゲーム開始直後にユーザーとディーラーインスタンスに2枚ずつカードを配る"""

    def _round_for_stand_or_burst(self, player: Player):
        """
        プレイヤーがスタンドもしくはバーストするまで待機する(繰り返す)
        :param player: ユーザーもしくはディーラーインスタンス
        """
        while player.is_stand or player.is_burst:
            player.hit()

            # ユーザーのターン
            if isinstance(player, User):
                self._show_initial_hands()

            # ディーラーのターン
            if isinstance(player, Dealer):
                self._show_final_hands()

    def _show_initial_hands(self):
        """ユーザーの全てのカードを表に、ディーラーの1枚のカードを表にする"""

    def _show_final_hands(self):
        """ユーザーとディーラーの全てのカードを表にする"""

    def _evaluate_judge(self):
        """勝敗を判定する"""

    @staticmethod
    def _is_user_replay_decision():
        """ユーザーに再戦するかどうか尋ねる"""
        return bool(input('再戦する場合は何か入力してエンターキーを押してください: '))

    def _ask_bets(self):
        """掛け金をユーザーに尋ねる"""

    def _distribute_bets(self):
        """掛け金を分配する"""


if __name__ == '__main__':
    game_manager = GameManager()
    game_manager.play_game()

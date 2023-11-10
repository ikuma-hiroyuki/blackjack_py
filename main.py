import os
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
        self._clear_terminal()
        print(self.art.title)
        input('エンターキーを押すとカードが配られます:')
        self._clear_terminal()
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

        # self._ask_bets()
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
                player.hand.append(Player.deck.card_list.pop())
                player.calculate_score()

    def _dealer_should_draw_card(self):
        """
        ディーラーがカードを引くべきか判定する

        ユーザーかディーラーがバーストしている場合は引かない
        ディーラーが17点以上かつユーザーに勝っている場合は引かない
        ユーザーが21点、ディーラーも21点の場合は引かない
        ディーラーが17点以上でユーザーに勝っている場合は引かない

        ディーラーが17点未満でもユーザーに勝っている場合は引く

        return: True: カードを引く, False: カードを引かない
        """

        if self.user.is_burst or self.dealer.is_burst:
            return False
        if self.dealer.score >= ScoreRules.DEALER_MIN_VALUE.value and self.dealer.score > self.user.score:
            return False
        if (self.user.score == self.dealer.score) and ScoreRules.BLACK_JACK_VALUE.value:
            return False

        return self.dealer.score < ScoreRules.DEALER_MIN_VALUE.value or self.dealer.score < self.user.score

    def _round_for_stand_or_burst(self, player: Player):
        """
        プレイヤーがスタンドもしくはバーストするまで待機する(繰り返す)
        :param player: ユーザーもしくはディーラーインスタンス
        """

        while True:
            if player.is_stand or player.is_burst:
                break

            if isinstance(player, User):
                if self.user.ask_stand():
                    player.stand()
                else:
                    player.hit()
                self._show_initial_hands()

            if isinstance(player, Dealer):
                while self._dealer_should_draw_card():
                    self._show_final_hands()
                    input('エンターキーを押してください:')
                    player.hit()
                player.stand()

    def _show_initial_hands(self):
        """ユーザーの全てのカードを表に、ディーラーの1枚のカードを表にする"""
        self._clear_terminal()
        self.user.show_all_face_and_score()
        self.dealer.show_card_face(num_visible_cards=1)
        print()

    def _show_final_hands(self):
        """ユーザーとディーラーの全てのカードを表にする"""
        self._clear_terminal()
        self.user.show_all_face_and_score()
        self.dealer.show_all_face_and_score()
        print()

    def _check_natural_blackjack(self, player: Player):
        """
        ナチュラルブラックジャックかどうか判定し、ユーザーがそうだった場合はAAを表示する
        :param player: ユーザーもしくはディーラーインスタンス
        """

        result = player.score == ScoreRules.BLACK_JACK_VALUE.value and len(player.hand) == 2
        if isinstance(player, User) and result:
            print(self.art.blackjack)
            input(f"{player.name}: ブラックジャック！")
            self.user_state.is_natural_blackjack = result

    def _evaluate_judge(self):
        """ユーザーの勝敗を判定し掛け金分配率を決定する"""
        self.user_state.game_result = self._judge_game_state()
        self.user_state.bet_distribute_rate = self._judge_distribute_bet()

    def _judge_game_state(self):
        """ユーザーの勝敗を判定する"""
        self._show_final_hands()

        if self.user.is_burst:
            print(self.art.burst)
            print(self.art.lose)
            return UserGameState.LOSE
        if self.dealer.is_burst:
            print(self.art.win)
            return UserGameState.WIN

        if self.user.score > self.dealer.score:
            print(self.art.win)
            return UserGameState.WIN
        elif self.user.score == self.dealer.score:
            print(self.art.draw)
            return UserGameState.DRAW
        else:
            print(self.art.lose)
            return UserGameState.LOSE

    def _judge_distribute_bet(self):
        """掛け金分配率を決定する"""
        if self.user_state.game_result == UserGameState.WIN:
            return BetRules.NATURAL_BLACK_JACK.value if self.user_state.is_natural_blackjack else BetRules.WIN.value
        elif self.user_state.game_result == UserGameState.DRAW:
            return BetRules.DRAW.value
        else:
            return BetRules.LOSE.value

    @staticmethod
    def _is_user_replay_decision():
        """ユーザーに再戦するかどうか尋ねる"""
        return not bool(input('終了する場合は何か入力してエンターキーを押してください: '))

    def _ask_bets(self):
        """掛け金をユーザーに尋ねる"""
        while True:
            try:
                bet_amount = int(input('掛け金を入力してください: '))
                if bet_amount < 0:
                    raise ValueError
                if bet_amount > self.user.money:
                    raise ValueError
            except ValueError:
                print('掛け金は0以上、かつ所持金以下の整数で入力してください')
            else:
                self.user_state.bet_amount = bet_amount
                self.user.money -= bet_amount
                break

    def _distribute_bets(self):
        """掛け金を分配する"""
        self.user.money += self.user_state.bet_amount * self.user_state.bet_distribute_rate

    def _reset_game(self):
        """ゲームをリセットする"""
        for player in self.players:
            player.reset_deal()
        self.user_state = UserState()

    @staticmethod
    def _clear_terminal():
        """ターミナルをクリアする"""
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == '__main__':
    game_manager = GameManager()
    game_manager.play_game()

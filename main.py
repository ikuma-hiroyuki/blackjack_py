import deal_helper
from art_manager import ArtManager
from deal_helper import ScoreRules, Odds
from player import User, Dealer, Player, UserGameStateEnum


class GameManager:
    """ブラックジャックのゲームを管理するクラス"""

    art = ArtManager()

    def __init__(self):
        self.user = User()
        self.dealer = Dealer()
        self.players = [self.user, self.dealer]  # ユーザー、ディーラーの順番でカードを配る
        self.judge_helper = self.GameJudge(self)
        self.show_helper = self.ShowArtAndMessage(self)

    def play_game(self):
        """ゲームを開始する"""
        deal_helper.clear_terminal()
        print(self.art.title)
        self._play_rounds()

    def _play_rounds(self):
        """各ラウンドをプレイする"""
        while self.user.money:
            self._round_of_game()
            if self.user.money and not deal_helper.ask_user_replay_decision():
                break

            if self.user.money:
                deal_helper.clear_terminal()
            self._reset_game()
        else:
            print('ゲームを終了します。')

    def _round_of_game(self):
        """ゲームを1回戦行う"""

        self.user.bet_amount = deal_helper.ask_bets(self.user.money)
        self._deal_card()

        self._user_draw_turn()
        self._dealer_draw_turn()

        self.judge_helper.evaluate_judge()
        self._distribute_bets()
        self.show_helper.show_bets_result()

    def _deal_card(self):
        """ゲーム開始直後にユーザーとディーラーインスタンスに2枚ずつカードを配る"""
        first_deal_card_num = 2
        for _ in range(first_deal_card_num):
            for player in self.players:
                player.hand.append(Player.deck.deal_a_card())
                player.calculate_score()

    def _user_draw_turn(self):
        """ユーザーのターン"""
        self.show_helper.show_user_turn_hands()
        while not (self.user.is_stand or self.user.is_burst):
            if deal_helper.ask_stand():
                self.user.stand()
            else:
                self.user.hit()
            self.show_helper.show_user_turn_hands()
            self.show_helper.show_blackjack_if_natural()

    def _dealer_draw_turn(self):
        """ディーラーのターン"""
        while self.judge_helper.dealer_should_draw_card():
            self.show_helper.show_dealer_turn_hands()
            input('ディーラーのターン。エンターキーを押してください:')
            self.dealer.hit()
        self.dealer.stand()
        self.show_helper.show_dealer_turn_hands()

    def _distribute_bets(self):
        """掛け金を分配する"""
        self.user.money += self.user.bet_amount * self.user.bet_distribute_rate

    def _reset_game(self):
        """1回戦分のゲームをリセットする"""
        for player in self.players:
            player.reset_deal()

    class GameJudge:
        """ディーラーがカードを引くかどうかや、ゲームの勝敗を判定するクラス"""

        def __init__(self, manager):
            self.user = manager.user
            self.dealer = manager.dealer
            self.art = manager.art

        def dealer_should_draw_card(self):
            """
            ディーラーがカードを引くべきか判定する

            ユーザーかディーラーがバーストしている場合は引かない

            以下、ディーラーが17点以上のケース
            ユーザーに勝っている場合は引かない
            ディーラーとユーザーが同点の場合、21点だったら引かないが、それ以外は引く

            ディーラーが17点未満の場合は常に引く(ユーザーバーストは除く)

            return: True: カードを引く, False: カードを引かない
            """

            if self.user.is_burst or self.dealer.is_burst:
                return False

            if self.dealer.score >= ScoreRules.DEALER_MIN.value:
                if self.dealer.score > self.user.score:
                    return False
                if self.dealer.score == self.user.score:
                    return self.dealer.score != ScoreRules.BLACK_JACK.value

            # ディーラーのスコアが17点未満の場合、常にカードを引く
            return True

        def evaluate_judge(self):
            """ユーザーの勝敗を判定し掛け金分配率を決定する"""
            ascii_art = self._judge_game_and_return_ascii_art()
            print(ascii_art)
            self.user.bet_distribute_rate = self._judge_distribute_bet()

        def _judge_game_and_return_ascii_art(self):
            """
            ユーザーの勝敗を判定しAAを返す
            return: アスキーアート
            """

            ascii_art = ""
            if self.user.is_burst:
                self.user.game_result = UserGameStateEnum.LOSE
                ascii_art = f'{self.art.burst}\n{self.art.lose}'
                return ascii_art

            if self.user.score > self.dealer.score or self.dealer.is_burst:
                ascii_art = self.art.win
                self.user.game_result = UserGameStateEnum.WIN
            elif self.user.score == self.dealer.score:
                ascii_art = self.art.draw
                self.user.game_result = UserGameStateEnum.DRAW
            else:
                ascii_art += self.art.lose
                self.user.game_result = UserGameStateEnum.LOSE

            return ascii_art

        def _judge_distribute_bet(self):
            """掛け金分配率を決定する"""
            if self.user.game_result == UserGameStateEnum.WIN:
                return Odds.NATURAL_BLACK_JACK.value if self.user.is_natural_blackjack else Odds.WIN.value
            elif self.user.game_result == UserGameStateEnum.DRAW:
                return Odds.DRAW.value
            else:
                return Odds.LOSE.value

    class ShowArtAndMessage:
        """AAとメッセージを表示するクラス"""

        def __init__(self, manager):
            self.user = manager.user
            self.dealer = manager.dealer
            self.art = manager.art

        def show_bets_result(self):
            """掛けの結果を表示する"""

            if self.user.bet_result_amount > 0:
                print(f'{self.user.bet_result_amount}円勝ち！')
            elif self.user.bet_result_amount == 0:
                print('引き分け')
            else:
                print(f'{-self.user.bet_result_amount}円負け...')

            if self.user.bet_result_amount != 0:
                print(f'所持金が{self.user.money}円になりました。\n')
            else:
                print(f'所持金は{self.user.money}円のままです。\n')

        def show_user_turn_hands(self):
            """ユーザーの全てのカードを表に、ディーラーの1枚のカードを表にする"""
            deal_helper.clear_terminal()
            print(f'掛け金: {self.user.bet_amount}')
            self.user.show_all_face_and_score()
            self.dealer.show_card_face(num_visible_cards=1)
            print()

        def show_dealer_turn_hands(self):
            """ユーザーとディーラーの全てのカードを表にする"""
            deal_helper.clear_terminal()
            print(f'掛け金: {self.user.bet_amount}')
            self.user.show_all_face_and_score()
            self.dealer.show_all_face_and_score()
            print()

        def show_blackjack_if_natural(self):
            """ユーザーがナチュラルブラックジャックだったらAAを表示する"""
            if self.user.is_natural_blackjack:
                print(self.art.blackjack)
                input("ブラックジャック！")


if __name__ == '__main__':
    GameManager().play_game()

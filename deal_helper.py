import os

from rules import ScoreRules


def ask_stand():
    """スタンドするかどうか尋ねる"""
    return bool(input(
        'スタンドする場合は何か入力してエンターキーを押してください。何も入力せずエンターキーを押すとヒットします。:\n'))


def ask_user_replay_decision():
    """ユーザーに再戦するかどうか尋ねる"""
    return not bool(input('終了する場合は何か入力してエンターキーを押してください: '))


def ask_bets(current_money):
    """
    掛け金をユーザーに尋ねる
    掛け金は1以上、かつ所持金以下の整数でなければならない
    param current_money: 現在の所持金
    """

    minimum_bet_amount = 1
    while True:
        try:
            bet_amount = int(input(f'掛け金を入力してください。現在の所持金 {current_money}: '))
            if bet_amount < minimum_bet_amount or bet_amount > current_money:
                raise ValueError
        except ValueError:
            print(f'掛け金は{minimum_bet_amount}円以上、かつ所持金以下の整数で入力してください。')
        else:
            return bet_amount


class ShowArtAndMessage:
    def __init__(self, game_manager):
        self.game_manager = game_manager

    def show_bets_result(self):
        """掛け金の結果を表示する"""

        if self.game_manager.user.bet_result_amount > 0:
            print(f'{self.game_manager.user.bet_result_amount}円勝ち！')
        else:
            print(f'{-self.game_manager.user.bet_result_amount}円負け...')

    def show_initial_hands(self):
        """ユーザーの全てのカードを表に、ディーラーの1枚のカードを表にする"""
        clear_terminal()
        print(f'掛け金: {self.game_manager.user.bet_amount}')
        self.game_manager.user.show_all_face_and_score()
        self.game_manager.dealer.show_card_face(num_visible_cards=1)
        print()

    def show_final_hands(self):
        """ユーザーとディーラーの全てのカードを表にする"""
        clear_terminal()
        print(f'掛け金: {self.game_manager.user.bet_amount}')
        self.game_manager.user.show_all_face_and_score()
        self.game_manager.dealer.show_all_face_and_score()
        print()

    def check_natural_blackjack(self):
        """
        ユーザーがナチュラルブラックジャックかどうか判定し、そうだったらAAを表示する
        """

        result = (self.game_manager.user.score == ScoreRules.BLACK_JACK_VALUE.value
                  and len(self.game_manager.user.hand) == 2)
        if result:
            print(self.game_manager.art.blackjack)
            input("ブラックジャック！")
            self.game_manager.user.is_natural_blackjack = result


def clear_terminal():
    """ターミナルをクリアする"""
    os.system('cls' if os.name == 'nt' else 'clear')

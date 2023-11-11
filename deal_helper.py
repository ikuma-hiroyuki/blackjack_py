import os
from enum import Enum, auto


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

    @property
    def bet_result_amount(self):
        """掛け金の結果を返す"""
        return int(self.bet_amount * self.bet_distribute_rate)


def ask_stand():
    """スタンドするかどうか尋ねる"""
    return bool(input(
        'スタンドする場合は何か入力してエンターキーを押してください。何も入力せずエンターキーを押すとヒットします。: '))


def ask_user_replay_decision():
    """ユーザーに再戦するかどうか尋ねる"""
    return not bool(input('終了する場合は何か入力してエンターキーを押してください: '))


def ask_bets(current_money):
    """
    掛け金をユーザーに尋ねる
    掛け金は0以上、かつ所持金以下の整数でなければならない
    """

    minimum_bet = 100
    while True:
        try:
            bet_amount = int(input(f'掛け金を入力してください。現在の所持金 {current_money}: '))
            if bet_amount < minimum_bet or bet_amount > current_money:
                raise ValueError
        except ValueError:
            print(f'掛け金は{minimum_bet}円以上、かつ所持金以下の整数で入力してください。')
        else:
            return bet_amount


def show_bets_result(user: UserState):
    """掛け金の結果を表示する"""
    if user.bet_result_amount > 0:
        print(f'{user.bet_result_amount}円勝ちました！')
    else:
        print(f'{-user.bet_result_amount}円負けました...')


def clear_terminal():
    """ターミナルをクリアする"""
    os.system('cls' if os.name == 'nt' else 'clear')

import os

from player import User


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


def show_bets_result(user: User):
    """
    掛け金の結果を表示する
    param user: Userインスタンス
    """
    if user.bet_result_amount > 0:
        print(f'{user.bet_result_amount}円勝！')
    else:
        print(f'{-user.bet_result_amount}円負け...')


def clear_terminal():
    """ターミナルをクリアする"""
    os.system('cls' if os.name == 'nt' else 'clear')

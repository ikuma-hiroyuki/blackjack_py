import random
from dataclasses import dataclass


@dataclass
class DealResult:
    """
    勝敗を示す列挙型
    """
    win: int = 0
    draw: int = 1
    lose: int = 2


@dataclass
class Score:
    dealer_min: int = 17
    dealer_max: int = 21


def get_default_dealer_cards(card_list):
    """
    ディーラーが最初に引く2枚のカードを取得する
    :param card_list: ディーラーがこれから引くことが可能なカードのリスト。要素が2つ以上あることが前提
    :return: ディーラーが最初に引いた2枚のカードのリスト
    """

    dealer_card_list = []
    for _ in range(2):
        card = random.choice(card_list)
        dealer_card_list.append(card)
        card_list.remove(card)
    return dealer_card_list


def set_dealer_final_card_list(dealer_card_list, card_list):
    """
    ディーラーがカードを引いていき、最終的なスコアを確定させる
    :param dealer_card_list: ディーラーがすでに引いている2枚目までのカード
    :param card_list: ディーラーがこれから引くことが可能なカードのリスト
    :return: 最終的なディーラーのカードのリストとスコアのタプル
    """

    # while 文内での処理用の初期値
    total_score = dealer_card_list[0].score + dealer_card_list[1].score  # A を常に11点とみなしたときの総得点
    dealer_score = total_score  # ディーラーのスコアとみなすべき値。最終的に戻り値になる。

    while dealer_score < Score.dealer_min:
        card = random.choice(card_list)
        dealer_card_list.append(card)
        card_list.remove(card)

        ace_count = len(list(filter(lambda x: x.is_ace, dealer_card_list)))  # A の枚数

        total_score += card.score
        dealer_score = get_dealer_current_score(total_score, ace_count)

    return dealer_card_list, dealer_score


def get_score(card_list):
    """
    手持ちのカードの得点を計算する
    :param card_list: 手持ちのカードのリスト
    :return: 得点
    """
    score = 0
    ace_count = 0
    for card in card_list:
        score += card.score
        if card.is_ace:
            ace_count += 1

    while ace_count > 0:
        score -= 10
        ace_count -= 1
    return score


def get_dealer_current_score(score, ace_count):
    """
    16を超えた値を受け取り、ディーラーのスコアを計算する
    :param score: 計算前のスコア
    :param ace_count:
    :return: 計算後のスコア
    """
    while score > Score.dealer_max and ace_count > 0:
        score -= 10
        ace_count -= 1
    return score


def get_deal_result(player_score, dealer_score):
    """
    プレイヤーとディーラーのスコアから勝敗を判定する
    :param player_score: プレイヤーのスコア
    :param dealer_score: ディーラーのスコア
    :return: 勝敗を示す列挙型
    """
    if player_score > Score.dealer_max:
        return DealResult.lose
    elif dealer_score > Score.dealer_max:
        return DealResult.win
    elif player_score > dealer_score:
        return DealResult.win
    elif player_score < dealer_score:
        return DealResult.lose
    elif player_score > Score.dealer_max:
        return DealResult.lose
    else:
        return DealResult.draw


def hit(card_list):
    """
    カードを1枚引く
    :param card_list: カードのリスト
    :return: カード
    """
    card = random.choice(card_list)
    card_list.remove(card)
    return card

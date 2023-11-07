import random

from card import Card
from deck import Deck


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.is_stand = False
        self.hand: list[Card] = []

    def hit(self):
        """カードを1枚引く"""
        random_index = random.randint(0, len(deck.card_list) - 1)
        self.hand.append(deck.card_list.pop(random_index))

    def stand(self):
        """スタンドしてスコアを確定させる"""
        self.is_stand = True
        self.calculate_score()

    def show_hand(self):
        """手札を表示する"""
        print(f'{self.name}の手札: ', end='')
        for card in self.hand:
            print(card, end=' ')

    def calculate_score(self):
        """手札のスコアを計算する"""
        initial_score = sum(card.score for card in self.hand)
        ace_count = sum(1 for card in self.hand if card.is_ace)

        adjusted_score = initial_score
        while adjusted_score > 21 and ace_count > 0:
            adjusted_score -= 10
            ace_count -= 1
        self.score = adjusted_score


class User(Player):
    def __init__(self):
        super().__init__('ユーザー')
        self.money = 0


if __name__ == '__main__':
    deck = Deck()
    user = User()

    while True:
        is_hit = input('Hit? (y/n)')
        if is_hit == 'y':
            user.hit()
            user.show_hand()
            print()
            print(deck.card_list)
        else:
            user.stand()
            print(user.score)
            break

    A1 = Card('♥', 'A', {'score': 11, 'is_ace': True})
    A2 = Card('♠', 'A', {'score': 11, 'is_ace': True})
    S10 = Card('♠', '10', {'score': 10, 'is_ace': False})
    user.hand = [A1, A2, S10]
    user.stand()
    user.show_hand()
    print(user.score)

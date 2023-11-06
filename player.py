import random

from deck import Deck


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.hand = []

    def hit(self):
        """カードを1枚引く"""

    def stand(self):
        """カードを引かずにターンを終了する"""

    def show_hand(self):
        """手札を表示する"""
        print(f'{self.name}の手札: ', end='')
        for card in self.hand:
            print(card, end=' ')
        print()


class User(Player):
    def hit(self):
        """カードを1枚引く"""
        random_index = random.randint(0, len(deck.card_list) - 1)
        self.hand.append(deck.card_list.pop(random_index))


if __name__ == '__main__':
    deck = Deck()
    user = User('ユーザー')
    while True:
        is_hit = input('Hit? (y/n)')
        if is_hit == 'y':
            user.hit()
            user.show_hand()
            print(deck.card_list)
        else:
            break

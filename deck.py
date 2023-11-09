from random import shuffle

from card import Card


class Deck:
    """
    デッキを表すクラス

    インスタンス化と同時にデッキ(ジョーカーを除く52枚のカード)を作り、シャッフルする
    """

    def __init__(self):
        self.card_list = []
        self._create_deck_and_shuffle()

    def _create_deck_and_shuffle(self):
        for suit in Card.SUITS:
            for rank, score in Card.CARD_SCORE.items():
                self.card_list.append(Card(suit, rank))
        shuffle(self.card_list)


if __name__ == '__main__':
    deck = Deck()
    for card in deck.card_list:
        print(card.get_card_art(show_face=True))
        print(card, card.score)
    print(deck.card_list)

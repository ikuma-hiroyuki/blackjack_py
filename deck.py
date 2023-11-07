from card import Card


class Deck:
    """デッキを表すクラス"""

    def __init__(self):
        self.card_list = []
        self._create_deck()

    def _create_deck(self):
        for suit in Card.SUITS:
            for rank, score in Card.CARD_SCORE.items():
                self.card_list.append(Card(suit, rank))


if __name__ == '__main__':
    deck = Deck()
    for card in deck.card_list:
        print(card.get_card_art(show_face=True))
        print(card, card.score)
    print(deck.card_list)

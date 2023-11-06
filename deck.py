from card import Card


class Deck:
    """デッキを表すクラス"""

    def __init__(self):
        self.card_list = []
        self._create_deck()

    def _create_deck(self):
        for suit in Card.SUITS:
            for rank, score in Card.CARD_SCORE.items():
                self.card_list.append(Card(suit, rank, score))


if __name__ == '__main__':
    deck = Deck()
    for card in deck.card_list:
        card.show_card(show_face=True, show_score=True)
        print(card)
    print(deck.card_list)

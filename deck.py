from card import Card


class Deck:
    SUITS = ['♠', '♣', '♥', '♦']
    CARD_SCORE = {
        'A': {'score': 11, 'is_ace': True},
        '2': {'score': 2},
        '3': {'score': 3},
        '4': {'score': 4},
        '5': {'score': 5},
        '6': {'score': 6},
        '7': {'score': 7},
        '8': {'score': 8},
        '9': {'score': 9},
        '10': {'score': 10},
        'J': {'score': 10},
        'Q': {'score': 10},
        'K': {'score': 10},
    }

    def __init__(self):
        self.card_list = []

    def create_card_list(self):
        for suit in self.SUITS:
            for rank, score in self.CARD_SCORE.items():
                self.card_list.append(Card(suit, rank, score))


if __name__ == '__main__':
    deck = Deck()
    deck.create_card_list()
    for card in deck.card_list:
        card.show_card(show_face=True, show_score=True)
        print(card)

    print(deck.card_list)

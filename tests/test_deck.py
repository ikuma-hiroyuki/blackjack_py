from colorama import Fore

from card import Card
from deck import Deck


class TestDeck:
    def test_create_card(self):
        """カードを生成して絵柄とスコア、色、エースかどうかをテストする"""

        # ハートのA
        hertz_ace = Card('♥', 'A')
        assert hertz_ace.suit == Fore.RED + '♥' + Fore.RESET
        assert hertz_ace.rank == Fore.RED + 'A' + Fore.RESET
        assert hertz_ace.score == 11
        assert hertz_ace.is_ace is True

        # スペードの10
        spade_10 = Card('♠', '10')
        assert spade_10.suit == Fore.RESET + '♠' + Fore.RESET
        assert spade_10.rank == Fore.RESET + '10' + Fore.RESET
        assert spade_10.score == 10
        assert spade_10.is_ace is False

    def test_create_deck(self):
        """デッキを生成して52枚の重複無しのカードが揃うかテスト"""
        assert len(set(Deck().card_list)) == 52

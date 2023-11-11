import pytest

import player
from card import Card
from rules import ScoreRules


class TestPlayer:
    @pytest.fixture(autouse=True)
    def create_test_case_cards(self):
        self.hertz_ace = Card('♥', 'A')
        self.spade_king = Card('♠', 'K')
        self.diamond_queen = Card('♦', 'Q')
        self.club_9 = Card('♣', '9')

    def test_stand(self):
        """スタンドしてスコアが正しく計算されているかテスト"""
        user = player.User()
        user.hand = [self.diamond_queen, self.club_9]
        user.stand()
        assert user.score == 19

    def test_hit(self):
        """ヒットしてスコアが正しく計算されているかテスト"""

        # ブラックジャック
        user1 = player.User()
        user1.hand = [self.hertz_ace, self.spade_king]
        user1.stand()
        assert user1.score == ScoreRules.BLACK_JACK_VALUE.value

        # エース、キング、9
        user2 = player.User()
        user2.hand = [self.hertz_ace, self.spade_king, self.club_9]
        user2.stand()
        assert user2.score == 20

        # エース、キング、クイーン
        user3 = player.User()
        user3.hand = [self.hertz_ace, self.spade_king, self.diamond_queen]
        user3.stand()
        assert user3.score == ScoreRules.BLACK_JACK_VALUE.value

        # エース、エース、エース、9
        user4 = player.User()
        user4.hand = [self.hertz_ace, self.hertz_ace, self.hertz_ace, self.club_9]
        user4.stand()
        assert user4.score == 12


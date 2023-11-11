import pytest

from main import GameManager


class TestGameManager:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.manager = GameManager()

    def test_dealer_should_draw_above_17_and_winning(self):
        """
        ディーラーがカードを引くべきかテストする
        ディーラーが17点以上かつユーザーに勝っている場合は引かない
        """

        self.manager.user.score = 16
        self.manager.user.is_burst = False
        self.manager.dealer.score = 17
        self.manager.dealer.is_burst = False

        assert self.manager._dealer_should_draw_card() is False

    def test_dealer_should_draw_under_17_winning(self):
        """ディーラーが17点未満でもユーザーに勝っている場合は引く"""
        self.manager.user.score = 4
        self.manager.user.is_burst = False
        self.manager.dealer.score = 16
        self.manager.dealer.is_burst = False

        assert self.manager._dealer_should_draw_card() is True

    def test_dealer_should_draw_user_burst(self):
        """ユーザーがバーストしている場合は引かない"""
        self.manager.user.score = 22
        self.manager.user.is_burst = True
        self.manager.dealer.score = 10

        assert self.manager._dealer_should_draw_card() is False

    def test_dealer_should_draw_burst(self):
        """ディーラーがバーストしている場合は引かない"""
        self.manager.dealer.score = 22
        self.manager.dealer.is_burst = True

        assert self.manager._dealer_should_draw_card() is False

    def test_dealer_should_draw_losing(self):
        """ディーラーがユーザーに負けている場合は引く"""
        self.manager.user.score = 20
        self.manager.user.is_burst = False
        self.manager.dealer.score = 19
        self.manager.dealer.is_burst = False

        assert self.manager._dealer_should_draw_card() is True

    def test_dealer_should_draw_tie_at_21(self):
        """ユーザーが21点、ディーラーも21点の場合は引かない"""
        self.manager.user.score = 21
        self.manager.user.is_burst = False
        self.manager.dealer.score = 21
        self.manager.dealer.is_burst = False

        assert self.manager._dealer_should_draw_card() is False

    def test_dealer_should_draw_tie_at_except_21(self):
        """ディーラーが21点、ユーザーも21点以外で同点の場合は引く"""
        self.manager.user.score = 20
        self.manager.user.is_burst = False
        self.manager.dealer.score = 20
        self.manager.dealer.is_burst = False

        assert self.manager._dealer_should_draw_card() is True

import pytest

from card import Card
from main import GameManager
from player import UserGameStateEnum


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

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_under_17_winning(self):
        """ディーラーが17点未満でもユーザーに勝っている場合は引く"""
        self.manager.user.score = 4
        self.manager.user.is_burst = False
        self.manager.dealer.score = 16
        self.manager.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is True

    def test_dealer_should_draw_user_burst(self):
        """ユーザーがバーストしている場合は引かない"""
        self.manager.user.score = 22
        self.manager.user.is_burst = True
        self.manager.dealer.score = 10

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_burst(self):
        """ディーラーがバーストしている場合は引かない"""
        self.manager.dealer.score = 22
        self.manager.dealer.is_burst = True

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_losing(self):
        """ディーラーがユーザーに負けている場合は引く"""
        self.manager.user.score = 20
        self.manager.user.is_burst = False
        self.manager.dealer.score = 19
        self.manager.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is True

    def test_dealer_should_draw_tie_at_21(self):
        """ユーザーが21点、ディーラーも21点の場合は引かない"""
        self.manager.user.score = 21
        self.manager.user.is_burst = False
        self.manager.dealer.score = 21
        self.manager.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_tie_at_except_21(self):
        """ディーラーが21点、ユーザーも21点以外で同点の場合は引く"""
        self.manager.user.score = 20
        self.manager.user.is_burst = False
        self.manager.dealer.score = 20
        self.manager.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is True

    def test_evaluate_game_user_win(self):
        """ユーザーが勝った場合の勝敗判定"""
        self.manager.user.score = 19
        self.manager.user.is_burst = False
        self.manager.user.is_stand = True

        self.manager.dealer.score = 16
        self.manager.dealer.is_burst = False
        self.manager.dealer.is_stand = True

        self.manager.judge_helper.evaluate_judge()

        assert self.manager.user.game_result == UserGameStateEnum.WIN

    def test_evaluate_game_user_lose(self):
        """ユーザーが負けた場合の勝敗判定"""
        self.manager.user.score = 16
        self.manager.user.is_burst = False
        self.manager.user.is_stand = True

        self.manager.dealer.score = 19
        self.manager.dealer.is_burst = False
        self.manager.dealer.is_stand = True

        self.manager.judge_helper.evaluate_judge()

        assert self.manager.user.game_result == UserGameStateEnum.LOSE

    def test_evaluate_game_user_draw(self):
        """ユーザーが引き分けた場合の勝敗判定"""
        self.manager.user.score = 16
        self.manager.user.is_burst = False
        self.manager.user.is_stand = True

        self.manager.dealer.score = 16
        self.manager.dealer.is_burst = False
        self.manager.dealer.is_stand = True

        self.manager.judge_helper.evaluate_judge()

        assert self.manager.user.game_result == UserGameStateEnum.DRAW

    def test_deal_card(self):
        """デッキをUser, Dealerで共有できているかテスト"""
        user_deck = self.manager.user.deck.card_list
        dealer_deck = self.manager.dealer.deck.card_list
        assert len(user_deck) == 52 and len(dealer_deck) == 52

        self.manager._deal_card()
        assert len(user_deck) == 48 and len(dealer_deck) == 48

        self.manager.user.hit()
        assert len(user_deck) == 47 and len(dealer_deck) == 47

        self.manager.dealer.hit()
        assert len(user_deck) == 46 and len(dealer_deck) == 46

        assert user_deck == dealer_deck


import pytest

from deal_helper import ScoreRules, Odds
from main import GameManager
from player import UserGameState


class TestGameManager:
    """ゲームの進行のテスト"""

    @pytest.fixture(autouse=True)
    def setup(self):
        self.manager = GameManager()
        self.user = self.manager.user
        self.dealer = self.manager.dealer

    def test_dealer_should_draw_above_17_and_winning(self):
        """
        ディーラーがカードを引くべきかテストする
        ディーラーが17点以上かつユーザーに勝っている場合は引かない
        """

        self.user.score = 16
        self.user.is_burst = False
        self.dealer.score = 17
        self.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_under_17_winning(self):
        """ディーラーが17点未満でもユーザーに勝っている場合は引く"""
        self.user.score = 4
        self.user.is_burst = False
        self.dealer.score = 16
        self.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is True

    def test_dealer_should_draw_user_burst(self):
        """ユーザーがバーストしている場合は引かない"""
        self.user.score = 22
        self.user.is_burst = True
        self.dealer.score = 10

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_burst(self):
        """ディーラーがバーストしている場合は引かない"""
        self.dealer.score = 22
        self.dealer.is_burst = True

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_losing(self):
        """ディーラーがユーザーに負けている場合は引く"""
        self.user.score = 20
        self.user.is_burst = False
        self.dealer.score = 19
        self.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is True

    def test_dealer_should_draw_tie_at_21(self):
        """ユーザーが21点、ディーラーも21点の場合は引かない"""
        self.user.score = 21
        self.user.is_burst = False
        self.dealer.score = 21
        self.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is False

    def test_dealer_should_draw_tie_at_except_21(self):
        """ディーラーが21点、ユーザーも21点以外で同点の場合は引く"""
        self.user.score = 20
        self.user.is_burst = False
        self.dealer.score = 20
        self.dealer.is_burst = False

        assert self.manager.judge_helper.dealer_should_draw_card() is True

    def test_evaluate_game_user_win(self):
        """ユーザーが勝った場合の勝敗判定"""
        self.user.score = 19
        self.user.is_burst = False
        self.user.is_stand = True

        self.dealer.score = 16
        self.dealer.is_burst = False
        self.dealer.is_stand = True

        self.manager.judge_helper.evaluate_judge()

        assert self.user.game_result == UserGameState.WIN

    def test_evaluate_game_user_lose(self):
        """ユーザーが負けた場合の勝敗判定"""
        self.user.score = 16
        self.user.is_burst = False
        self.user.is_stand = True

        self.dealer.score = 19
        self.dealer.is_burst = False
        self.dealer.is_stand = True

        self.manager.judge_helper.evaluate_judge()

        assert self.user.game_result == UserGameState.LOSE

    def test_evaluate_game_user_draw(self):
        """ユーザーが引き分けた場合の勝敗判定"""
        self.user.score = 16
        self.user.is_burst = False
        self.user.is_stand = True

        self.dealer.score = 16
        self.dealer.is_burst = False
        self.dealer.is_stand = True

        self.manager.judge_helper.evaluate_judge()

        assert self.user.game_result == UserGameState.DRAW

    def test_evaluate_game_user_and_dealer_burst(self):
        """双方がバーストした場合の勝敗判定"""
        self.user.score = 22
        self.user.is_burst = True
        self.user.is_stand = True

        self.dealer.score = 22
        self.dealer.is_burst = True
        self.dealer.is_stand = True

        self.manager.judge_helper.evaluate_judge()

        assert self.user.game_result == UserGameState.LOSE

    def test_deal_card(self):
        """デッキをUser, Dealerで共有できているかテスト"""
        user_deck = self.user._deck.card_list
        dealer_deck = self.dealer._deck.card_list
        assert len(user_deck) == 52 and len(dealer_deck) == 52

        self.manager._deal_card()
        assert len(user_deck) == 48 and len(dealer_deck) == 48

        self.manager.user.hit()
        assert len(user_deck) == 47 and len(dealer_deck) == 47

        self.manager.dealer.hit()
        assert len(user_deck) == 46 and len(dealer_deck) == 46

        assert user_deck == dealer_deck

    def test_odds_natural_bj(self):
        """ナチュラルブラックジャックの掛け金分配率テスト"""
        self.user.is_natural_blackjack = True
        self.user.score = ScoreRules.BLACK_JACK.value
        self.dealer.score = 20
        self.manager.judge_helper.evaluate_judge()
        assert self.user.bet_distribute_rate == Odds.NATURAL_BLACK_JACK.value

    def test_odds_win(self):
        """勝利時の掛け金分配率テスト"""
        self.user.is_natural_blackjack = False
        self.user.score = 20
        self.dealer.score = 19
        self.manager.judge_helper.evaluate_judge()
        assert self.user.bet_distribute_rate == Odds.WIN.value

    def test_odds_draw(self):
        """引き分け時の掛け金分配率テスト"""
        self.user.is_natural_blackjack = False
        self.user.score = 20
        self.dealer.score = 20
        self.manager.judge_helper.evaluate_judge()
        assert self.user.bet_distribute_rate == Odds.DRAW.value

    def test_odds_lose(self):
        """敗北時の掛け金分配率テスト"""
        self.user.is_natural_blackjack = False
        self.user.score = 19
        self.dealer.score = 20
        self.manager.judge_helper.evaluate_judge()
        assert self.user.bet_distribute_rate == Odds.LOSE.value

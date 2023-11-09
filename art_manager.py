from pathlib import Path


class ArtManager:
    """アスキーアートを管理するクラス"""

    _ART_DIR = Path(__file__).absolute().parent / "ascii_art"

    def __init__(self):
        self._cache = {}

    def _get_ascii_art(self, name):
        """
        指定した名前のアスキーアートを読み込む
        :param name: アスキーアートのファイル名
        """

        if name not in self._cache:
            with Path.open(self._ART_DIR / name, "r", encoding="utf-8") as f:
                self._cache[name] = f.read()
        return self._cache[name]

    @property
    def card_face(self):
        """カードの表面のアスキーアートを返す"""
        return self._get_ascii_art('card_face.txt')

    @property
    def card_back(self):
        """カードの裏面のアスキーアートを返す"""
        return self._get_ascii_art('card_back.txt')

    @property
    def blackjack(self):
        """ブラックジャックのアスキーアートを返す"""
        return self._get_ascii_art('blackjack.txt')

    @property
    def win(self):
        """勝利のアスキーアートを返す"""
        return self._get_ascii_art('win.txt')

    @property
    def lose(self):
        """敗北のアスキーアートを返す"""
        return self._get_ascii_art('lose.txt')

    @property
    def draw(self):
        """引き分けのアスキーアートを返す"""
        return self._get_ascii_art('draw.txt')

    @property
    def burst(self):
        """バーストのアスキーアートを返す"""
        return self._get_ascii_art('burst.txt')

    @property
    def title(self):
        """タイトルのアスキーアートを返す"""
        return self._get_ascii_art('title.txt')

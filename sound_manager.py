from kivy.core.audio import SoundLoader
from game_config import SOUND_DIR, SOUND_BG_MUSIC, SOUND_CLICK_TAP, SOUND_DRAW, SOUND_WIN, SOUND_CLICK_BTN, VOLUME_DEFAULT

"""
Quản lý nhạc nền & hiệu ứng âm thanh
==========================================================
• Tải file âm thanh một lần, tái sử dụng suốt vòng lặp app.
• Phát nhạc nền lặp (loop) & SFX (tap, win, draw, click).
"""
class SoundManager:
# ------------------------------------------------------------------ #
#                           SOUND MANAGER                           #
# ------------------------------------------------------------------ #
    def __init__(self, auto_play_bg=True):
        # Nhạc & hiệu ứng
        self.bg   = SoundLoader.load(f"{SOUND_DIR}/{SOUND_BG_MUSIC}")
        self.tap  = SoundLoader.load(f"{SOUND_DIR}/{SOUND_CLICK_TAP}")
        self.win  = SoundLoader.load(f"{SOUND_DIR}/{SOUND_WIN}")
        self.draw = SoundLoader.load(f"{SOUND_DIR}/{SOUND_DRAW}")
        self.click = SoundLoader.load(f"{SOUND_DIR}/{SOUND_CLICK_BTN}")
        for s in (self.bg, self.tap, self.win, self.draw):
            if s: s.volume = VOLUME_DEFAULT

        if auto_play_bg and self.bg:
            self.bg.loop = True
            self.bg.play()

    # ----------------------- WRAPPER METHODS -------------------------
    def play_tap(self):  self._safe(self.tap)
    def play_win(self):  self._safe(self.win)
    def play_draw(self): self._safe(self.draw)
    def play_click(self):
        """Click button: stop & play để luôn phát từ đầu."""
        if self.click:
            self.click.stop()  
            self.click.play()

    # ----------------------- HELPER STATIC ---------------------------
    @staticmethod
    def _safe(snd):
        """Phát âm thanh nếu hợp lệ, bỏ qua lỗi IO."""
        try:
            if snd:
                snd.seek(0)
                snd.play()
        except Exception:
            pass

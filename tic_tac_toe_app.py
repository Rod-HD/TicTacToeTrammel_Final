from kivy.config import Config
Config.set('graphics', 'minimum_width', 400)
Config.set('graphics', 'minimum_height', 600)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from themes import Theme
from home_screen import HomeScreen
from game_screen import GameScreen
from game_config import DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_WIN_LEN, DEFAULT_NUM_OBSTACLES, SCREEN_GAME, SCREEN_HOME, DEFAULT_DIFFICULTY

"""
Ứng dụng Kivy chính
===========================================
• Tạo ScreenManager chứa HomeScreen & GameScreen
• Xử lý vòng lặp ván cờ, luân chuyển theme, dừng nhạc nền khi rời màn
"""
class TicTacToeApp(App):
    """Ứng dụng gói toàn bộ game Tic-Tac-Toe."""
    # --------------------------- BUILD ------------------------------
    def build(self):
        # Đặt lại về theme đầu tiên
        Theme.reset()
        self.sm = ScreenManager(transition=FadeTransition())
        # HomeScreen sẽ gọi start_game để khởi tạo GameScreen
        self.sm.add_widget(HomeScreen(name=SCREEN_HOME))
        return self.sm
    
    # ---------------------- KHỞI TẠO GAME ---------------------------
    def start_game(self, mode: str, difficulty: str = DEFAULT_DIFFICULTY,
                   rows: int = DEFAULT_ROWS, cols: int = DEFAULT_COLS,
                   win_len: int = DEFAULT_WIN_LEN, num_obstacles: int = DEFAULT_NUM_OBSTACLES):
        """Tạo GameScreen mới & chuyển tới nó."""
        # 1) Dừng nhạc nền màn chơi trước (nếu có)
        if self.sm.has_screen(SCREEN_GAME):
            old = self.sm.get_screen(SCREEN_GAME)
            if hasattr(old, 'game_widget') and hasattr(old.game_widget, '_sounds'):
                if old.game_widget._sounds.bg:
                    old.game_widget._sounds.bg.stop()
            self.sm.remove_widget(old)

        # 2) Tạo màn mới
        game_screen = GameScreen(
            mode, difficulty,
            rows=rows, cols=cols,
            win_len=win_len, num_obstacles=num_obstacles,
            on_game_end=self.on_game_end,
            name=SCREEN_GAME,
        )
        self.sm.add_widget(game_screen)
        self.sm.current = SCREEN_GAME

    # ----------------------- CALLBACK GAME END ----------------------
    def on_game_end(self):
        """Được gọi khi kết thúc 1 trận để chuyển sang theme tiếp theo."""
        next_theme = Theme.next_theme()
        # Cập nhật theme cho màn hình game hiện tại
        if self.sm.has_screen(SCREEN_GAME):
            gs = self.sm.get_screen(SCREEN_GAME)
            if hasattr(gs, 'apply_theme'):
                gs.apply_theme(next_theme)

    # --------------------------- HOME -------------------------------
    def go_home(self):
        """Trở về Home & dừng nhạc nền nếu cần."""
        if self.sm.has_screen(SCREEN_GAME):
            gs = self.sm.get_screen(SCREEN_GAME)
            if hasattr(gs, 'game_widget') and hasattr(gs.game_widget, '_sounds'):
                if gs.game_widget._sounds.bg:
                    gs.game_widget._sounds.bg.stop()
        self.sm.current = SCREEN_HOME

    # --------------------------- EXIT -------------------------------
    def on_stop(self):
        # Dừng âm thanh khi app đóng
        if self.sm.current == SCREEN_GAME and self.sm.has_screen(SCREEN_GAME):
            gs = self.sm.get_screen(SCREEN_GAME)
            if hasattr(gs, 'game_widget') and hasattr(gs.game_widget, '_sounds'):
                if gs.game_widget._sounds.bg:
                    gs.game_widget._sounds.bg.stop()

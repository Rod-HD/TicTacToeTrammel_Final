"""
Màn hình chứa một ván Tic-Tac-Toe
======================================================
Nhúng TicTacToeLayout trong một Screen của Kivy và bổ sung nút
Back to Menu có màu sắc đồng bộ với các nút control khác.
"""

# ----------------------------- IMPORTS ------------------------------ #
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.app import App

from utils import style_round_button, enable_press_darken, enable_click_sound
from game_factory import create_game
from game_config import (
    BTN_RGBA,            
    BACK_LABEL,          
    DEFAULT_FONT,        
    BACK_BTN_W,          
    BACK_BTN_H,          
)

# ------------------------------------------------------------------ #
#                           KIVY SCREEN                             #
# ------------------------------------------------------------------ #

class GameScreen(Screen):
    """`Screen` bao trọn một instance trò chơi Tic‑Tac‑Toe."""

    # --------------------------- KHỞI TẠO -----------------------------
    def __init__(
        self,
        mode: str,
        difficulty: str = "medium",
        rows: int = 5,
        cols: int = 5,
        win_len: int = 4,
        num_obstacles: int = 5,
        **kwargs,
    ):
        super().__init__(**kwargs)

        # 1) Sinh layout trò chơi qua factory
        self.game_widget = create_game(
            mode,
            difficulty,
            rows=rows,
            cols=cols,
            win_len=win_len,
            num_obstacles=num_obstacles,
        )
        self.add_widget(self.game_widget)

        # 2) Tạo nút Back‑to‑Menu (đồng bộ UI)
        back_btn = Button(
            text=f"[b]{BACK_LABEL}[/b]",  # Dùng markup để in đậm
            markup=True,
            font_name=DEFAULT_FONT,
            size_hint=(None, None),
            width=BACK_BTN_W,
            height=BACK_BTN_H,
            pos_hint={"x": 0.02, "top": 0.98},
        )
        style_round_button(back_btn, rgba=BTN_RGBA)   # Bo góc + màu
        enable_press_darken(back_btn, factor=0.5)     # Tối màu khi nhấn
        enable_click_sound(back_btn)                  # Âm thanh click
        back_btn.bind(on_release=lambda *_: App.get_running_app().go_home())
        self.add_widget(back_btn)

    # ----------------------- PUBLIC METHOD ---------------------------
    def apply_theme(self, theme):
        """Truyền theme mới xuống `TicTacToeLayout`."""
        if hasattr(self, "game_widget") and hasattr(self.game_widget, "apply_theme"):
            self.game_widget.apply_theme(theme)

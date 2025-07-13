from __future__ import annotations
from typing import Optional, Tuple

from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Rectangle
from kivy.properties import StringProperty

from board_widget    import BoardWidget
from board           import Board
from game_controller import GameController
from game_state      import GameState
from themes          import Theme
from sound_manager   import SoundManager
from utils           import style_round_button, enable_press_darken, enable_click_sound
from game_config     import (
    DIM_ALPHA, BTN_RGBA, BTN_W, BTN_H, FONT_BOLD,
    STATUS_X_TURN, STATUS_X_WIN, STATUS_O_WIN, STATUS_DRAW,
) 

"""
Layout tổng hợp cho một ván cờ
========================================================
Gồm:
• BoardWidget (view bàn cờ)
• 3 nút điều khiển (Restart, Shuffle Obstacles, Undo)
• Nhãn trạng thái (ai tới lượt, ai thắng, hoà)
• Observer lắng nghe thay đổi từ GameController
"""

class TicTacToeLayout(FloatLayout):
    """Bố cục giao diện cho một ván Tic‑Tac‑Toe."""
    status_message = StringProperty(STATUS_X_TURN)

    # ------------------- BUTTON CƠ SỞ (INNER CLASS) -----------------
    class _BaseBtn(Button):
        def __init__(self, text: str, rgba, **kw):
            super().__init__(**kw)
            self.markup, self.text = True, text
            self.font_name         = FONT_BOLD
            self.size_hint         = (None, None)
            self.width, self.height = BTN_W, BTN_H
            self.halign = self.valign = "center"
            self.text_size = (self.width - 20, None)
            style_round_button(self, rgba=rgba)
            enable_press_darken(self, factor=0.5) 
            enable_click_sound(self)
            self.bind(size=self._fit)

        def _fit(self, *_):
            self.text_size = (self.width - 20, None)

    # ------------------ BUTTON CỤ THỂ (INNER CLASS) -----------------
    class _RestartBtn(_BaseBtn):
        def __init__(self, cb):
            super().__init__("[b]Restart[/b]", BTN_RGBA,
                             pos_hint={"x": 0.02, "y": 0.02},
                             on_release=lambda *_: cb())
            self.disabled, self.opacity = True, DIM_ALPHA

    class _ShuffleBtn(_BaseBtn):
        def __init__(self, cb):
            super().__init__("[b]Shuffle\nObstacles[/b]", BTN_RGBA,
                             pos_hint={"right": 0.98, "y": 0.02},
                             on_release=lambda *_: cb())

    class _UndoBtn(_BaseBtn):
        def __init__(self, cb):
            super().__init__("[b]Undo[/b]", BTN_RGBA,
                             pos_hint={"right": 0.98, "top": 0.98},
                             on_release=lambda *_: cb())
            self.disabled, self.opacity = True, DIM_ALPHA

    # --------------------------- KHỞI TẠO ----------------------------
    def __init__(self, controller: GameController, theme: Theme, **kw):
        super().__init__(**kw)
        self._controller, self._board = controller, controller._board
        self._state = GameState.IN_PROGRESS
        self._sounds = SoundManager()
        self._theme = theme

        # --- Background --------------------------------------------
        with self.canvas.before:
            self._bg = Rectangle(source=theme.bg, pos=self.pos, size=self.size)
        self.bind(size=self._sync_bg, pos=self._sync_bg)

        # --- Khung trung tâm chứa BoardWidget ----------------------
        self._frame = FloatLayout(size_hint=(None, None))
        self.add_widget(self._frame)

        self._grid = BoardWidget(self._board, on_cell_cb=self._controller.play)
        self._grid.pos_hint = {"center_x": .5, "center_y": .5}
        self._frame.add_widget(self._grid)
        self._grid.reset(self._board)

        # --- Nhãn trạng thái dưới cùng -----------------------------
        self._status_lbl = Label(
            text=self.status_message, markup=True,
            font_name=FONT_BOLD, font_size="18sp",
            size_hint=(None, None), width=BTN_W,
            pos_hint={"center_x": 0.5, "y": 0.02},
            halign="center", valign="middle",
        )

        # text_size auto-fit
        self._status_lbl.bind(size=lambda *a:
                              self._status_lbl.setter("text_size")
                              (self._status_lbl, (self._status_lbl.width, None)))
        self.add_widget(self._status_lbl)

        # --- 3 nút điều khiển --------------------------------------
        self._restart_btn = self._RestartBtn(self._restart_game); self.add_widget(self._restart_btn)
        self._shuffle_btn = self._ShuffleBtn(self._shuffle_obstacles); self.add_widget(self._shuffle_btn)
        self._undo_btn   = self._UndoBtn(self._undo_move);   self.add_widget(self._undo_btn)

        # --- Geometry ---------------------------------------------
        Window.bind(on_resize=lambda *_: self._update_geometry())
        self._update_geometry()

        # --- Đăng ký lắng nghe controller -------------------------
        self._controller.register(self)

    # ------------------------------------------------------------------ #
    #                          THEME UPDATE                              #
    # ------------------------------------------------------------------ #
    def apply_theme(self, theme):
        """Controller gọi khi chuyển theme mới."""
        self._theme = theme
        self._bg.source = theme.bg           
        self._grid.reset(self._board)   

    # ------------------------------------------------------------------ #
    #                     OBSERVER CALLBACKS (Model → View)              #
    # ------------------------------------------------------------------ #
    def on_board_change(self, coords: Tuple[int, int], symbol: str):
        self._grid.update_cell(coords, symbol)
        self._sounds.play_tap()
        self._update_undo_btn()

    def on_state_change(self, state: GameState, next_turn: Optional[str]):
        msg = {
            GameState.X_WON: STATUS_X_WIN,
            GameState.O_WON: STATUS_O_WIN,
            GameState.DRAW : STATUS_DRAW,
        }.get(state, f"[b]{next_turn}'s turn[/b]")
        self._status_lbl.text = msg

        finished = state in (GameState.X_WON, GameState.O_WON, GameState.DRAW)
        if finished:
            self._sounds.play_win() if state != GameState.DRAW else self._sounds.play_draw()
            self._restart_btn.disabled, self._restart_btn.opacity = False, 1
            self._shuffle_btn.disabled = True
        else:
            self._restart_btn.disabled, self._restart_btn.opacity = True, DIM_ALPHA
            self._shuffle_btn.disabled = False

        # ▼ Khoá / mở các ô trên bàn cờ
        for cell in self._grid._cells.values():    
            cell.disabled = finished               
        self._dim_board(finished)

        self._state = state          
        self._update_undo_btn()

    # ------------------------------------------------------------------ #
    #                      BUTTON HANDLERS (View → Controller)           #
    # ------------------------------------------------------------------ #
    def _dim_board(self, dim: bool):
            """Mờ / hiện rõ toàn bộ ô trên bàn cờ + khóa hoặc mở click."""
            alpha = DIM_ALPHA if dim else 1
            for cell in self._grid._cells.values():
                cell.disabled = dim
                cell.opacity  = alpha

    def _update_undo_btn(self):
        """Bật / tắt Undo tùy vào trạng thái ván và lịch sử nước đi."""
        has_move = self._board.has_moves
        in_play   = self._state is GameState.IN_PROGRESS
        enabled   = has_move and in_play

        self._undo_btn.disabled = not enabled
        self._undo_btn.opacity  = 1 if enabled else DIM_ALPHA

    def _restart_game(self):
        # 1) Chọn theme kế tiếp
        self._theme = Theme.next_theme()

        # 2) Cập nhật background
        self._bg.source = self._theme.bg

        # 3) Reset logic & khung cờ như cũ
        self._controller.reset()
        self._grid.reset(self._board)   # XOCell sẽ tự lấy Theme.current()
        self._dim_board(False)
        # 4) Khôi phục trạng thái nút / nhãn
        self._restart_btn.disabled, self._restart_btn.opacity = True, DIM_ALPHA
        self._shuffle_btn.disabled = False
        self._status_lbl.text = "[b]X's turn[/b]"

    def _shuffle_obstacles(self):
        self._controller.reshuffle_obstacles(); self._grid.reset(self._board)

    def _undo_move(self):
        self._controller.undo()
        self._grid.reset(self._board)
        self._update_undo_btn()

    # ------------------------------------------------------------------ #
    #                           GEOMETRY                                 #
    # ------------------------------------------------------------------ #
    def _update_geometry(self, *_):
        win_w, win_h = Window.size
        side = min(win_w, win_h)               
        x = (win_w - side) / 2
        y = (win_h - side) / 2
        self._frame.size, self._frame.pos = (side, side), (x, y)

    def _sync_bg(self, *_): self._bg.pos, self._bg.size = self.pos, self.size

"""
xo_cell.py  – one class only: XOCell
A single square on the grid.  Handles tinting the obstacle sprite the
same colour as the main buttons.
"""

from typing import Callable
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.properties import StringProperty
from themes import Theme
from game_config import CELL_SIZE, PLAYER_X, PLAYER_O, OBSTACLE_SYMBOL, BTN_RGBA

"""
Ô đơn lưới Tic-Tac-Toe
-----------------------------------
View thuần Kivy, kết hợp ButtonBehavior + Image:

* Hiển thị icon X / O / obstacle / ô trống tuỳ symbol.
* Phát sự kiện click về controller qua callback.
* Tự lấy hình ảnh theo Theme.current().

Không chứa logic thắng-thua, chỉ UI.
"""
class XOCell(ButtonBehavior, Image):
    """Clickable ô lưới; gọi callback (row, col) khi người dùng nhấn."""
    mark = StringProperty("") # Trạng thái hiện tại: '', X, O, #

    def __init__(self, row: int, col: int,
                 on_press_cb: Callable[[int, int], None],
                 **kwargs):
        super().__init__(**kwargs)
        self.row, self.col = row, col
        self._cb           = on_press_cb

        self.size_hint = (None, None)
        self.size      = (CELL_SIZE, CELL_SIZE)
        self.allow_stretch = True
        self.keep_ratio    = False

        self.set_mark("")          

    # ---------------------- SỰ KIỆN USER TAP ----------------------- #
    def on_release(self):
        """Khi ô được nhấp: báo về controller."""
        self._cb(self.row, self.col)

    # ------------------------ CẬP NHẬT SPRITE ----------------------- #
    def set_mark(self, symbol: str) -> None:
        """Đổi icon & màu theo ký hiệu symbol."""
        theme = Theme.current()      
        if symbol == PLAYER_X:
            self.source = theme.x_icon
            self.color  = (1, 1, 1, 1)
        elif symbol == PLAYER_O:
            self.source = theme.o_icon
            self.color  = (1, 1, 1, 1)
        elif symbol == OBSTACLE_SYMBOL:
            self.source = theme.obs_icon
            self.color  = BTN_RGBA    # tint cùng màu nút control
        else:                         # ô trống
            self.source = theme.cell_bg
            self.color  = (1, 1, 1, 1)
        self.mark = symbol

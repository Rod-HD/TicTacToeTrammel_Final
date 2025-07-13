from board import Board
from game_controller import GameController
from themes import Theme
from layout import TicTacToeLayout
from game_config import DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_WIN_LEN, DEFAULT_NUM_OBSTACLES

"""
Tạo instance trò chơi hoàn chỉnh
=======================================================
Cung cấp hàm create_game để sinh:
1. Board: model (state + luật)
2. GameControlle: controller (điều phối lượt & AI)
3. Theme: chủ đề giao diện (màu, hình ảnh)
4. TicTacToeLayout: layout Kivy hoàn chỉnh sẵn dùng cho App.
"""

def create_game(mode       : str = "friend",
                difficulty : str = "medium",
                element    : str = "wood",
                rows       : int = DEFAULT_ROWS,
                cols       : int = DEFAULT_COLS,
                win_len    : int = DEFAULT_WIN_LEN,
                num_obstacles: int = DEFAULT_NUM_OBSTACLES) -> TicTacToeLayout:

    board      = Board(rows=rows, cols=cols, win_len=win_len, num_obstacles=num_obstacles)
    controller = GameController(board, mode, difficulty)
    Theme.reset()
    theme = Theme.current()
    #theme      = Theme(element)
    return TicTacToeLayout(controller, theme)

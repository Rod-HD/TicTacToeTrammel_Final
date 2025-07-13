import random
from typing import List, Tuple, Set, Optional

from game_config import (
    DEFAULT_ROWS, DEFAULT_COLS, DEFAULT_WIN_LEN, DEFAULT_NUM_OBSTACLES,
    EMPTY_SYMBOL, OBSTACLE_SYMBOL, PLAYER_X, PLAYER_O, DRAW_SYMBOL,
)


class Board:
    """Mô hình dữ liệu của trò chơi - lưu trạng thái và kiểm soát luật."""
    # ------------------------------------------------------------------ #
    #                           HẰNG SỐ                                  #
    # ------------------------------------------------------------------ #
    EMPTY: str = EMPTY_SYMBOL
    OBSTACLE: str = OBSTACLE_SYMBOL
    _PLAYERS: tuple[str, str] = (PLAYER_X, PLAYER_O)

    # ------------------------------------------------------------------ #
    #                           KHỞI TẠO                                  #
    # ------------------------------------------------------------------ #
    def __init__(
        self,
        rows: int = DEFAULT_ROWS,
        cols: int = DEFAULT_COLS,
        win_len: int = DEFAULT_WIN_LEN,
        num_obstacles: int = DEFAULT_NUM_OBSTACLES,
    ) -> None:
        self._rows = rows
        self._cols = cols
        self._win_len = win_len
        self._num_obstacles = num_obstacles

        self._history: List[Tuple[int, int, str]] = []
        self._last_placed_sym: Optional[str] = None
        self._current_winner: Optional[str] = None

        self.reset()

    # ------------------------------------------------------------------ #
    #                     THUỘC TÍNH TRẠNG THÁI (READ‑ONLY)              #
    # ------------------------------------------------------------------ #
    @property
    def rows(self) -> int:
        return self._rows

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def has_moves(self) -> bool:
        """Trả True nếu đã có ít nhất một nước đi lưu trong _history."""
        return bool(self._history)

    @property
    def history_len(self) -> int:
        return len(self._history)

    @property
    def grid_snapshot(self):
        """Trả bản sao lưới để quan sát mà không sửa được."""
        return [row[:] for row in self._grid]

    @property
    def obstacles(self) -> Set[Tuple[int, int]]:
        return {
            (i, j)
            for i in range(self._rows)
            for j in range(self._cols)
            if self._grid[i][j] == self.OBSTACLE
        }

    # ------------------------------------------------------------------ #
    #                        HÀNH ĐỘNG TRÊN BÀN                           #
    # ------------------------------------------------------------------ #
    def is_empty(self, i: int, j: int) -> bool:
        return (i, j) in self._legal

    def place(self, i: int, j: int, symbol: str) -> bool:
        """Đánh quân *symbol* tại (i, j) – giữ nguyên tên hàm."""
        if (i, j) not in self._legal:
            return False

        # Lưu trạng thái cũ để có thể undo
        original_symbol = self._grid[i][j]
        self._history.append((i, j, original_symbol))

        # Cập nhật lưới và tập hợp ô trống
        self._grid[i][j] = symbol
        self._legal.remove((i, j))
        self._last_placed_sym = symbol

        # Kiểm tra thắng / hòa
        if self.has_winner(i, j, symbol):
            self._current_winner = symbol
        elif self.is_draw():
            self._current_winner = DRAW_SYMBOL
        return True

    def undo_last_move(self) -> None:
        if not self._history:
            return
        last_r, last_c, prev_symbol = self._history.pop()
        self._grid[last_r][last_c] = prev_symbol
        self._legal.add((last_r, last_c))

        self._current_winner = None
        self._last_placed_sym = None
        if self._history:
            prev_r, prev_c, _ = self._history[-1]
            self._last_placed_sym = self._grid[prev_r][prev_c]

    def get_legal_moves(self) -> Set[Tuple[int, int]]:
        return self._legal.copy()

    # ------------------------------------------------------------------ #
    #                   KIỂM TRA KẾT QUẢ                                 #
    # ------------------------------------------------------------------ #
    def has_winner(self, i: int, j: int, symbol: str) -> bool:
        directions = [
            (0, 1),   # ngang
            (1, 0),   # dọc
            (1, 1),   # chéo chính
            (1, -1),  # chéo phụ
        ]
        for dx, dy in directions:
            if self._count_streak(i, j, dx, dy, symbol) >= self._win_len:
                return True
        return False

    def _count_streak(self, i: int, j: int, dx: int, dy: int, symbol: str) -> int:
        """Đếm liên tiếp symbol theo hướng (dx,dy) qua (i,j)."""
        streak = 0
        for k in range(-self._win_len + 1, self._win_len):
            r, c = i + k * dx, j + k * dy
            if 0 <= r < self._rows and 0 <= c < self._cols and self._grid[r][c] == symbol:
                streak += 1
                if streak >= self._win_len:
                    return streak
            else:
                streak = 0
        return streak

    def has_winner_any(self) -> bool:
        return self._current_winner in self._PLAYERS

    def get_winner_symbol(self) -> Optional[str]:
        return self._current_winner

    def is_draw(self) -> bool:
        return not self._legal and not self.has_winner_any()

    def is_full(self) -> bool:
        return not self._legal

    # ------------------------------------------------------------------ #
    #                    THIẾT LẬP / LÀM MỚI BÀN CỜ                       #
    # ------------------------------------------------------------------ #
    def reset(self) -> None:
        self._grid: List[List[str]] = [[self.EMPTY for _ in range(self._cols)] for _ in range(self._rows)]
        self._history.clear()
        self._last_placed_sym = None
        self._current_winner = None

        self._place_obstacles()
        self._legal: Set[Tuple[int, int]] = {
            (i, j)
            for i in range(self._rows)
            for j in range(self._cols)
            if self._grid[i][j] == self.EMPTY
        }

    def reshuffle_obstacles(self) -> None:
        for i in range(self._rows):
            for j in range(self._cols):
                if self._grid[i][j] == self.OBSTACLE:
                    self._grid[i][j] = self.EMPTY
                    self._legal.add((i, j))

        self._place_obstacles()
        self._legal = {
            (i, j)
            for i in range(self._rows)
            for j in range(self._cols)
            if self._grid[i][j] == self.EMPTY
        }
        self._history.clear()
        self._last_placed_sym = None
        self._current_winner = None

    def clear_marks(self) -> None:
        for i in range(self._rows):
            for j in range(self._cols):
                if self._grid[i][j] not in (self.EMPTY, self.OBSTACLE):
                    self._grid[i][j] = self.EMPTY
                    self._legal.add((i, j))
        self._history.clear()
        self._last_placed_sym = None
        self._current_winner = None

    # ------------------------------------------------------------------ #
    #                        TRUY VẤN ĐƠN LẺ                             #
    # ------------------------------------------------------------------ #
    def get_mark(self, row: int, col: int) -> str:
        return self._grid[row][col]

    # ------------------------------------------------------------------ #
    #                      HÀM NỘI BỘ HỖ TRỢ                             #
    # ------------------------------------------------------------------ #
    def _place_obstacles(self) -> None:
        placed = 0
        while placed < self._num_obstacles:
            i, j = random.randrange(self._rows), random.randrange(self._cols)
            if self._grid[i][j] == self.EMPTY:
                self._grid[i][j] = self.OBSTACLE
                placed += 1

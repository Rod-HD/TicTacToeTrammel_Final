from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window

from board import Board
from xo_cell import XOCell
from game_config import CELL_SIZE, MARGIN_X, MARGIN_Y


class BoardWidget(GridLayout):
    """
    View thuần túy (không chứa logic xử lý luật chơi).

    Nhiệm vụ:
    1. Vẽ lưới ô dựa trên đối tượng Board.
    2. Lắng nghe click của người dùng và chuyển tiếp sự kiện đến controller thông qua callback.
    3. Tự điều chỉnh kích thước theo cửa sổ để tương thích nhiều màn hình.
    """

    # ------------------------------------------------------------------ #
    #                           KHỞI TẠO                                 #
    # ------------------------------------------------------------------ #
    def __init__(self, board: Board, on_cell_cb, **kw):
        """
        board : Board
            Trạng thái hiện tại của bàn cờ.
        on_cell_cb : Callable[[int, int], None]
            Hàm callback được gọi khi người dùng nhấn vào một ô.
        """
        super().__init__(
            rows=board.rows,
            cols=board.cols,
            spacing=0,
            size_hint=(None, None),
            **kw,
        )

        # Kích thước ban đầu: dựa vào CELL_SIZE cấu hình
        self.size = (CELL_SIZE * board.cols, CELL_SIZE * board.rows)

        # Lưu trữ tham chiếu tới các ô => dễ cập nhật hiển thị
        self._cells: dict[tuple[int, int], XOCell] = {}

        # Tạo các ô
        for row in range(board.rows):
            for col in range(board.cols):
                cell = XOCell(row, col, on_cell_cb)
                self.add_widget(cell)
                self._cells[(row, col)] = cell

        # Gắn sự kiện resize cửa sổ
        Window.bind(on_resize=self._on_window_resize)

        # Cập nhật kích thước ngay lần đầu chạy
        self._on_window_resize(Window, Window.width, Window.height)

    # ------------------------------------------------------------------ #
    #                         HÀM HỖ TRỢ RIÊNG                           #
    # ------------------------------------------------------------------ #
    def _on_window_resize(self, window, width, height) -> None:
        """Tính lại kích thước mỗi ô cho vừa cửa sổ."""

        # Diện tích vẽ = tổng trừ lề để tránh đụng nút/viền
        avail_w = width - MARGIN_X
        avail_h = height - MARGIN_Y

        # Lấy cạnh nhỏ hơn để ô không vượt khung
        cell_size = avail_h // self.rows if avail_h < avail_w else avail_w // self.cols

        # Cập nhật kích thước layout
        self.size = (cell_size * self.cols, cell_size * self.rows)

        # Cập nhật từng ô
        for cell in self.children:
            cell.size = (cell_size, cell_size)

    # ------------------------------------------------------------------ #
    #                           PUBLIC API                               #
    # ------------------------------------------------------------------ #
    def reset(self, board: Board) -> None:
        """Vẽ lại toàn bộ bàn cờ dựa trên trạng thái mới."""
        for (row, col), cell in self._cells.items():
            cell.set_mark(board.get_mark(row, col))

    def update_cell(self, coords: tuple[int, int], symbol: str) -> None:
        """Cập nhật nhanh một ô khi người chơi vừa đánh."""
        row, col = coords
        if (row, col) in self._cells:
            self._cells[(row, col)].set_mark(symbol)

from typing import Tuple, Optional, Protocol
from game_state import GameState

"""
Giao diện Observer cho trò chơi
=====================================================
Định nghĩa giao thức (Protocol) mà mọi observer (UI, âm thanh, logger…) cần
triển khai để nhận thông báo từ GameController.
- Không chứa logic; chỉ quy định chữ ký hai phương thức.
"""

class GameObserver(Protocol):
    def on_board_change(self, coords: Tuple[int, int], symbol: str) -> None:
        """Được gọi khi một ô trên bàn cờ thay đổi.

        coords : Tuple[int, int]
            Toạ độ (row, col) của ô vừa cập nhật.
        symbol : str
            Ký hiệu mới tại ô.
        """
        ...

    def on_state_change(self, state: GameState, next_turn: Optional[str]) -> None:
        """Được gọi khi trạng thái ván cờ thay đổi.

        state : GameState
            Trạng thái hiện tại (IN_PROGRESS, X_WON,…).
        next_turn : Optional[str]
            Ký hiệu người chơi kế tiếp (hoặc None nếu ván đã kết thúc).
        """
        ...

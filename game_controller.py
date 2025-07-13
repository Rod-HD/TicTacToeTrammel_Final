"""
Điều phối lượt chơi và AI
====================================================
Cầu nối giữa **View** (UI Kivy) và **Model** (`Board`).
- Quản lý thứ tự lượt, trạng thái trận, và gọi AI khi chơi với máy.
- Gửi thông báo (observer pattern) cho các thành phần UI/âm thanh.
"""

from typing import List, Tuple
from kivy.clock import Clock
import logging

from board import Board
from minimax import MinimaxAI
from game_state import GameState
from game_observer import GameObserver
from game_config import PLAYER_X, PLAYER_O, MODE_BOT, MODE_FRIEND, DELAY_AI_MOVE, DEFAULT_AI_LEVEL

# ----------------------------- LOGGING SETUP --------------------------- #
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class GameController:
    # ------------------------------------------------------------------ #
    #                               KHỞI TẠO                            #
    # ------------------------------------------------------------------ #
    def __init__(self, board: Board, mode: str = MODE_FRIEND, difficulty: str = DEFAULT_AI_LEVEL) -> None:
        """
        board : Board
            Thể hiện của lớp Board (model) đang được điều khiển.
        mode : str
            Chế độ chơi - 'Play with Friend' (2 người) hoặc 'Play vs Bot' (đánh với AI).
        difficulty : str
            Độ khó AI (chuỗi tuỳ theo MinimaxAI, ví dụ 'easy' | 'medium' | 'hard').
        """
        self._board      = board                    # Model gốc
        self._current    = PLAYER_X                 # Người chơi bắt đầu
        self._state      = GameState.IN_PROGRESS    # Trạng thái ván hiện tại
        self._observers: List[GameObserver] = []    # Danh sách lắng nghe

        self._mode       = mode
        self._difficulty = difficulty

        if mode == MODE_BOT:
            # Khởi tạo AI chỉ khi cần
            self._ai        = MinimaxAI(difficulty)
            self._human_sym = PLAYER_X
            self._ai_sym    = PLAYER_O
        else:
            self._ai = None

    # ------------------------------------------------------------------ #
    #                           PUBLIC API                              #
    # ------------------------------------------------------------------ #
    def reset(self) -> None:
        """Bắt đầu ván mới: xoá bàn, tạo obstacle và trả lượt cho X."""
        self._board.reset()
        self._current = PLAYER_X
        self._state   = GameState.IN_PROGRESS
        logger.debug("Game reset: current player = X, state = IN_PROGRESS")

        # Thông báo mọi observer vẽ lại bàn (nếu có _grid)
        for obs in self._observers:
            if hasattr(obs, "_grid"):
                obs._grid.reset(self._board)
        self._notify_state()

    def undo(self) -> None:
        """Hoàn tác nước đi cuối cùng và cập nhật view."""
        if self._state is not GameState.IN_PROGRESS:
            return  # Chỉ undo khi ván đang diễn ra

        self._board.undo_last_move()

        # Đảo lượt người chơi
        self._current = PLAYER_O if self._current == PLAYER_X else PLAYER_X
        self._state   = GameState.IN_PROGRESS

        # Thông báo UI vẽ lại
        for obs in self._observers:
            if hasattr(obs, "_grid"):
                obs._grid.reset(self._board)
        self._notify_state()

    def play(self, i: int, j: int) -> None:
        """Xử lý nước đi của người chơi hiện tại."""
        # 1) Từ chối nếu ván đã kết thúc
        if self._state is not GameState.IN_PROGRESS:
            logger.debug("Move ignored: the game is already finished.")
            return

        logger.debug(f"Attempting move ({i},{j}) bởi {self._current}")
        # 2) Thử đặt quân lên model
        if not self._board.place(i, j, self._current):
            logger.warning(f"Invalid move tại ({i},{j})")
            return

        # 3) Cập nhật UI qua observer
        self._notify_board((i, j), self._current)

        # 4) Kiểm tra thắng / hoà / đổi lượt
        if self._board.has_winner(i, j, self._current):
            self._state = GameState.X_WON if self._current == PLAYER_X else GameState.O_WON
            logger.debug(f"Winner detected: {self._state}")
        elif self._board.is_draw():
            self._state = GameState.DRAW
            logger.debug("Game ended in a draw")
        else:
            # Đổi lượt
            self._current = PLAYER_O if self._current == PLAYER_X else PLAYER_X
            logger.debug(f"Turn switched to {self._current}")
            # Nếu tới lượt AI -> lên lịch cho AI đánh (delay 0.2s)
            if self._mode == MODE_BOT and self._current == self._ai_sym:
                Clock.schedule_once(lambda *_: self._ai_move(), DELAY_AI_MOVE)

        # 5) Thông báo trạng thái mới
        self._notify_state()

    def reshuffle_obstacles(self) -> None:
        """Đảo vị trí obstacle khi ván đang chơi."""
        if self._state is not GameState.IN_PROGRESS:
            return
        self._board.reshuffle_obstacles()
        for obs in self._observers:
            if hasattr(obs, "_grid"):
                obs._grid.reset(self._board)

    def register(self, obs: GameObserver) -> None:
        """Thêm observer (UI / âm thanh) nhận thông báo."""
        self._observers.append(obs)
        logger.debug(f"Registered observer: {obs}")
        obs.on_state_change(self._state, self._current)

    # ------------------------------------------------------------------ #
    #                           INTERNAL HELPERS                         #
    # ------------------------------------------------------------------ #
    def _notify_board(self, coords: Tuple[int, int], symbol: str) -> None:
        """Gửi tín hiệu cập nhật một ô cho tất cả observer."""
        for o in self._observers:
            o.on_board_change(coords, symbol)

    def _notify_state(self) -> None:
        """Gửi tín hiệu thay đổi trạng thái ván cho mọi observer."""
        next_p = None if self._state is not GameState.IN_PROGRESS else self._current
        for o in self._observers:
            o.on_state_change(self._state, next_p)

    def _ai_move(self) -> None:
        """Hàm callback cho nước đi của AI."""
        if not self._ai:
            logger.error("AI chưa được khởi tạo")
            return
        move = self._ai.best(self._board, self._ai_sym, self._human_sym)
        logger.debug(f"AI chọn nước {move}")
        self.play(*move)  # Gọi lại play để xử lý bình thường

    # ------------------------------------------------------------------ #
    #                           READ‑ONLY PROPS                          #
    # ------------------------------------------------------------------ #
    @property
    def state(self) -> GameState:
        """Trạng thái hiện tại của ván cờ."""
        return self._state

    @property
    def current_player(self) -> str:
        """Ký hiệu người sẽ đánh kế tiếp (hoặc người vừa thắng)."""
        return self._current

    @property
    def board(self) -> Board:
        """Truy cập model Board."""
        return self._board

from __future__ import annotations
import copy
from board           import Board
from game_controller import GameController
from game_config     import MODE_FRIEND, PLAYER_X, PLAYER_O
from game_state      import GameState


# ---------- trợ giúp ----------
def make_ctrl(rows=3, cols=3, win_len=3, num_obstacles=0) -> GameController:
    bd = Board(rows, cols, win_len, num_obstacles)
    return GameController(bd, MODE_FRIEND)        # chỉ truyền board


# ----------------- test 1 ------------------
def test_no_move_after_finish():
    ctrl = make_ctrl()
    bd   = ctrl.board        

    win_seq = [(0, 0), (1, 0),
               (0, 1), (1, 1),
               (0, 2)]          # X thắng

    for r, c in win_seq:
        ctrl.play(r, c)

    assert ctrl.state == GameState.X_WON

    grid_before = bd.grid_snapshot               # bản sao an toàn

    ctrl.play(2, 2)                              # thử đánh thêm

    assert ctrl.state == GameState.X_WON
    assert bd.grid_snapshot == grid_before       # không đổi


# ----------------- test 2 ------------------
def test_undo_logic():
    ctrl = make_ctrl()
    bd   = ctrl.board

    ctrl.play(0, 0)          # X
    ctrl.play(1, 1)          # O

    assert ctrl.current_player == PLAYER_X
    assert bd.history_len == 2

    ctrl.undo()

    assert bd.is_empty(1, 1)
    assert bd.history_len == 1
    assert ctrl.current_player == PLAYER_O
    assert ctrl.state == GameState.IN_PROGRESS

import pytest
from board import Board, OBSTACLE_SYMBOL   # OBSTACLE_SYMBOL dùng để so sánh snapshot

X, O = "X", "O"


# ---------- fixture Board mặc định ---------- #
@pytest.fixture
def b():
    return Board(rows=3, cols=3, win_len=3, num_obstacles=0)


# ------------------ has_winner ---------------- #
@pytest.mark.parametrize("line", [
    [(0, 0), (0, 1), (0, 2)],      # row
    [(0, 0), (1, 0), (2, 0)],      # col
    [(0, 0), (1, 1), (2, 2)],      # main diag
    [(0, 2), (1, 1), (2, 0)],      # anti diag
])
def test_has_winner(line):
    bd = Board(3, 3, 3, 0)
    for r, c in line:
        assert bd.place(r, c, X)
    assert bd.has_winner(*line[-1], X)
    assert bd.has_winner_any()
    assert bd.get_winner_symbol() == X


# -------------------- draw -------------------- #
def test_draw(b):
    moves = [
        (0, 0, X), (0, 1, O), (0, 2, X),
        (1, 0, X), (1, 1, O), (1, 2, O),
        (2, 0, O), (2, 1, X), (2, 2, X),
    ]
    for r, c, sym in moves:
        assert b.place(r, c, sym)
    assert b.is_draw()


# --------------- undo_last_move -------------- #
def test_undo_last_move(b):
    b.place(0, 0, X)
    b.place(1, 1, O)
    b.undo_last_move()
    assert b.is_empty(1, 1)
    assert b.history_len == 1        
    assert b.get_winner_symbol() is None


# ----------- reshuffle_obstacles ------------- #
def test_reshuffle_obstacles():
    board = Board(5, 5, 4, num_obstacles=5)

    before = board.obstacles           

    board.reshuffle_obstacles()

    after = board.obstacles

    assert len(before) == len(after) == 5
    assert before != after              # vị trí phải thay đổi

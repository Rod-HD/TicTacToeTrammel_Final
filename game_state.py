from enum import Enum, auto

# Liệt kê trạng thái ván cờ
class GameState(Enum):
    IN_PROGRESS = auto()
    X_WON       = auto()
    O_WON       = auto()
    DRAW        = auto()

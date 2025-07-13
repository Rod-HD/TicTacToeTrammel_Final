from pathlib import Path
from game_config import NAMES_THEMES, BG_THEME,CELL_THEME, X_THEME, O_THEME, OBSTACLE_THEME, ASSETS

"""
Quản lý chủ đề (theme) hình ảnh
================================================
Cung cấp class Theme để:
• Xác định đường dẫn tới background, icon X/O, ô trống, obstacle
• Cho phép xoay vòng (next) và reset về theme đầu tiên
"""
class Theme:
    """Đối tượng chủ đề giao diện (ảnh, icon) cho một ván cờ."""
    _index: int = 0                 # Chỉ số theme hiện tại (class‑level)
    NAMES = NAMES_THEMES            # Danh sách theme sẵn có (from config)

    # --------------------------- KHỞI TẠO ----------------------------
    def __init__(self, name: str):
        base = Path(ASSETS) / name  # Thư mục theme: assets/<name>/
        self.name     = name
        self.bg       = str(base / BG_THEME)        # Background
        self.cell_bg  = str(base / CELL_THEME)      # Hình ô trống
        self.x_icon   = str(base / X_THEME)         # Icon X
        self.o_icon   = str(base / O_THEME)         # Icon O
        self.obs_icon = str(base / OBSTACLE_THEME)  # Icon chướng ngại

    # ---------------------- CLASSMETHOD HELPERS ----------------------
    @classmethod
    def current(cls) -> "Theme":
        """Trả về Theme hiện tại (không tạo new nếu cùng index)."""
        name = cls.NAMES[cls._index]
        return cls(name)

    @classmethod
    def next_theme(cls) -> "Theme":
        """Chuyển sang theme tiếp theo (xoay vòng) và trả về instance mới."""
        cls._index = (cls._index + 1) % len(cls.NAMES)
        return cls.current()

    @classmethod
    def reset(cls):
        """Đặt lại index về đầu danh sách."""
        cls._index = 0
        return cls.current()

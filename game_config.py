from kivy.resources import resource_find
"""
Trung tâm cấu hình & hằng số
=================================================
Thay đổi một chỗ sẽ ảnh hưởng toàn bộ dự án.
"""

# ------------------------------------------------------------------ #
#                           KIVY FONT PATH                           #
# ------------------------------------------------------------------ #
# Font hệ thống (dùng trong LabelBase.register nếu muốn tên tắt)
FONT_BOLD    = resource_find('data/fonts/Roboto-Bold.ttf')
FONT_LOBSTER = resource_find('assets/fonts/Lobster-Regular.ttf')
DEFAULT_FONT = "Roboto-Bold"

# ------------------------------------------------------------------ #
#                       ÂM THANH & THƯ MỤC ASSET                     #
# ------------------------------------------------------------------ #
ASSETS_DIR             = "assets"
SOUND_DIR              = "sounds"

SOUND_BG_MUSIC         = "bg_music.ogg"
SOUND_CLICK_TAP        = "click_tap.wav"
SOUND_DRAW             = "draw.wav"
SOUND_WIN              = "win.wav"
SOUND_CLICK_BTN        = "click_btn.wav"
VOLUME_DEFAULT         = 0.4

# ------------------------------------------------------------------ #
#                         QUY TẮC BÀN CỜ & GAME                      #
# ------------------------------------------------------------------ #

DEFAULT_ROWS           = 5
DEFAULT_COLS           = 5
DEFAULT_WIN_LEN        = 4
DEFAULT_NUM_OBSTACLES  = 5

EMPTY_SYMBOL           = "."
OBSTACLE_SYMBOL        = "#"
PLAYER_X               = "X"
PLAYER_O               = "O"
DRAW_SYMBOL            = 'D' 

# ------------------------------------------------------------------ #
#                       CHẾ ĐỘ CHƠI & ĐỘ KHÓ AI                      #
# ------------------------------------------------------------------ #
MODE_FRIEND            = "friend"
MODE_BOT               = "bot"

DIFFICULTY_EASY        = "easy"
DIFFICULTY_MEDIUM      = "medium"
DIFFICULTY_HARD        = "hard"
DEFAULT_DIFFICULTY     = "medium"
DEFAULT_AI_LEVEL       = "medium"
DELAY_AI_MOVE          = 0.2  # Thời gian AI suy nghĩ (giây)

# ------------------------------------------------------------------ #
#                          LAYOUT & STYLE                             #
# ------------------------------------------------------------------ #
CELL_SIZE              = 60
BTN_W, BTN_H           = 260, 60
BACK_BTN_W, BACK_BTN_H = 200, 60

# màu chung cho nút control & obstacle tint
BTN_RGBA               = (0.75, 0.60, 0.45, 1)
DIM_ALPHA              = 0.5

# Lề (px) để Board vừa cửa sổ nhưng tránh đụng cạnh
MARGIN_X = 100
MARGIN_Y = 200

# Kích cỡ font tiện dùng ở nhiều nơi
TITLE_FS   = '80sp'
SETTING_FS = '18sp'
BUTTON_FS  = '32sp'

# ------------------------------------------------------------------ #
#                            THEME / SKIN                            #
# ------------------------------------------------------------------ #
DEFAULT_THEME          = "wood"
NAMES_THEMES = [
    "metal",
    "wood",
    "water",
    "fire",
    "earth"
]
BG_THEME       = "bg.png"
CELL_THEME     = "cell.png"
X_THEME        = "x.png"
O_THEME        = "o.png"
OBSTACLE_THEME = "obstacle.png"
ASSETS         = "assets" # tiện alias cho Theme class

# Ảnh nền mặc định khi chưa load Theme
DEFAULT_BG_IMAGE   = "assets/wood/bg.png"

# ------------------------------------------------------------------ #
#                          TEXT / LABELS                              #
# ------------------------------------------------------------------ #
BACK_LABEL = "Back to Menu"
TITLE_TEXT         = "Tic Tac Toe"
BTN_PLAY_BOT_LABEL = "Play vs Bot"
BTN_PLAY_F_LABEL   = "Play with Friend"

STATUS_X_TURN = "[b]X's turn[/b]"
STATUS_X_WIN = "[b]X wins![/b]"
STATUS_O_WIN = "[b]O wins![/b]"
STATUS_DRAW = "[b]Draw![/b]"

# ------------------------------------------------------------------ #
#                        SCREEN MANAGER NAMES                        #
# ------------------------------------------------------------------ #
SCREEN_HOME = "home"
SCREEN_GAME = "game"

# ------------------------------------------------------------------ #
#                               POPUP                                #
# ------------------------------------------------------------------ #
BG_ERROR = 'assets/images/error.png'
SELECT_DIF = 'assets/images/select_dif.png'
BTN_BOT = 'assets/images/btn_bot.png'
BTN_FRIEND = 'assets/images/btn_friend.png'

# ------------------------------------------------------------------ #
#                       GIÁ TRỊ PHỤ KHÁC                             #
# ------------------------------------------------------------------ #
RESTART                = 60


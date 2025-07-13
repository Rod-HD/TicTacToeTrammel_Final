"""
Central place for every tweakable constant.
Edit here once and the whole game picks up the change.
"""
from kivy.resources import resource_find

FONT_BOLD = resource_find('data/fonts/Roboto-Bold.ttf')
FONT_LOBSTER = resource_find('assets/fonts/Lobster-Regular.ttf')
BG_ERROR = 'assets/images/error.png'
SELECT_DIF = 'assets/images/select_dif.png'
BTN_BOT = 'assets/images/btn_bot.png'
BTN_FRIEND = 'assets/images/btn_friend.png'
# ── board size & rules ────────────────────────────────────────────
DEFAULT_ROWS           = 5
DEFAULT_COLS           = 5
DEFAULT_WIN_LEN        = 4
DEFAULT_NUM_OBSTACLES  = 5

EMPTY_SYMBOL           = "."
OBSTACLE_SYMBOL        = "#"
PLAYER_X               = "X"
PLAYER_O               = "O"

# ── play modes & AI difficulty ────────────────────────────────────
MODE_FRIEND            = "friend"
MODE_BOT               = "bot"

DIFFICULTY_EASY        = "easy"
DIFFICULTY_MEDIUM      = "medium"
DIFFICULTY_HARD        = "hard"

# ── UI ­values ────────────────────────────────────────────────────
CELL_SIZE              = 60
DEFAULT_THEME          = "wood"
RESTART                = 60

# ── asset & sound locations ───────────────────────────────────────
ASSETS_DIR             = "assets"
SOUND_DIR              = "sounds"

SOUND_BG_MUSIC         = "bg_music.ogg"
SOUND_CLICK_TAP        = "click_tap.wav"
SOUND_DRAW             = "draw.wav"
SOUND_WIN              = "win.wav"
SOUND_CLICK_BTN        = "click_btn.wav"

# ── theme names ──────────────────────────────────────────────────
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
ASSETS         = "assets"

# ----- shared style -----──
BTN_RGBA = (0.75, 0.60, 0.45, 1)
DIM_ALPHA = 0.5
BOLD_FONT  = "Roboto-Bold"
BTN_RGBA   = (0.75, 0.60, 0.45, 1)
BTN_W, BTN_H = 260, 60

# Hằng số lề (px) để layout không chạm cạnh cửa sổ
MARGIN_X = 100
MARGIN_Y = 200

PLAYER_X = 'X'
PLAYER_O = 'O'
DRAW_SYMBOL = 'D' 

DELAY_AI_MOVE = 0.2  # Thời gian AI suy nghĩ (giây)
DEFAULT_AI_LEVEL = "medium"

BACK_LABEL = "Back to Menu"
DEFAULT_FONT = "Roboto-Bold"
BACK_BTN_W = 200
BACK_BTN_H = 60

DEFAULT_BG_IMAGE   = "assets/wood/bg.png"
TITLE_TEXT         = "Tic Tac Toe"
BTN_PLAY_BOT_LABEL = "Play vs Bot"
BTN_PLAY_F_LABEL   = "Play with Friend"
TITLE_FS   = '80sp'
SETTING_FS = '18sp'
BUTTON_FS  = '32sp'

STATUS_X_TURN = "[b]X's turn[/b]"
STATUS_X_WIN = "[b]X wins![/b]"
STATUS_O_WIN = "[b]O wins![/b]"
STATUS_DRAW = "[b]Draw![/b]"

VOLUME_DEFAULT = 0.4

DEFAULT_DIFFICULTY = "medium"
SCREEN_HOME = "home"
SCREEN_GAME = "game"
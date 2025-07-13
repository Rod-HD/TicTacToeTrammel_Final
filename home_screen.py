# homescreen.py
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout # Thêm import này
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.app import App
from kivy.uix.textinput import TextInput
from utils import style_round_button, style_round_texture_widget, style_round_widget, enable_press_darken, enable_click_sound
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.scrollview import ScrollView
from game_config import FONT_BOLD, FONT_LOBSTER, BG_ERROR, SELECT_DIF, BTN_BOT, BTN_FRIEND, TITLE_FS, SETTING_FS, BUTTON_FS
from kivy.metrics import dp

"""
Màn hình chính chọn chế độ và cấu hình bàn cờ
====================================================================
View khởi đầu: nhập kích thước bàn, chọn chế độ Bot/Friend, chọn
độ khó AI, hiển thị popup lỗi.
"""

class HomeScreen(Screen):
    """Màn hình Home – nhập tuỳ chọn và khởi động game."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # --- NỀN -------------------------------------------------------
        root = FloatLayout()
        with root.canvas.before:
            self.bg = Rectangle(source='assets/wood/bg.png', pos=root.pos, size=root.size)
        root.bind(size=self._update_bg, pos=self._update_bg)
        
        main_layout = BoxLayout(orientation='vertical', padding=50, spacing=30)
        
        # --- TIÊU ĐỀ ---------------------------------------------------
        title = Label(
            text='[b]Tic Tac Toe[/b]',
            font_size=TITLE_FS,
            font_name=FONT_LOBSTER,  
            size_hint=(1, 0.2),
            markup=True,
            color=(1, 1, 1, 1) # Màu chữ trắng để nổi bật trên nền gỗ
        )
        
        # --- KHUNG INPUT ----------------------------------------------
        settings_container = GridLayout(
            cols=2,
            spacing=10,
            padding=10,
            size_hint=(0.8, 0.4), 
            pos_hint={'center_x': 0.5} 
        )

        def create_setting_row(label_text, default_value):
            """Tạo một dòng Label + TextInput."""
            label = Label(
                markup=True,
                text=f'[b]{label_text}[/b]',
                halign='right', valign='middle',
                size_hint_x=.4,
                font_size=SETTING_FS,
                color=(.9, .9, .9, 1)
            )

            settings_container.add_widget(label)

            # TextInput cho nhập số
            text_input = TextInput(
                text=str(default_value),
                input_filter='int',
                multiline=False,
                size_hint_x=.6,
                height='40dp',
                font_size='20sp',

                background_normal='',
                background_active='',
                background_color=(0.30, 0.20, 0.10, 0.8),
                foreground_color=(1, 1, 1, 1),     
                cursor_color=(1, 1, 1, 1),        

                halign='center',
                padding=[10, 10, 10, 10]
            )

            # --- Căn giữa dọc -------------------------------------------------------
            def _center_vertically(widget, *_):
                widget.padding_y = [(widget.height - widget.line_height) / 2]

            # chạy 1 lần và mỗi khi thay đổi size / font
            _center_vertically(text_input)
            text_input.bind(size=_center_vertically, font_size=_center_vertically)

            settings_container.add_widget(text_input)
            return text_input
        
        # Tạo các TextInput cho Rows, Columns, Win Length, Obstacles
        self.rows_input = create_setting_row('Rows:', 5)
        self.cols_input = create_setting_row('Columns:', 5)
        self.win_len_input = create_setting_row('Win Length:', 4)
        self.num_obstacles_input = create_setting_row('Number of Obstacles:', 5)
        
        # --- NÚT CHƠI --------------------------------------------------
        button_container = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint=(0.8, 0.3),
            pos_hint={'center_x': 0.5}
        )
        
        # --- Play vs Bot button ---
        vs_bot_btn = Button(
            text='[b]Play vs Bot[/b]',
            markup=True,
            font_size=BUTTON_FS,
            size_hint=(1, .45),
            color=(0.0, 0.17, 0.36, 1),
            background_normal='', 
            background_down='',
            background_color=(0,0,0,0)
        )

        # Bo góc + màu
        style_round_texture_widget(
            vs_bot_btn,
            image_path=BTN_BOT,
            radius=12
        )
        # Hiệu ứng nhấn làm tối đi + âm thanh
        enable_press_darken(vs_bot_btn, factor=0.5)
        enable_click_sound(vs_bot_btn)
        vs_bot_btn.bind(on_release=self.show_difficulty_popup)

        # --- Play with Friend button ---
        vs_friend_btn = Button(
            markup=True,
            text='[b]Play with Friend[/b]',
            font_size=BUTTON_FS,
            size_hint=(1, .45),
            color = (0.8, 0.333, 0.0, 1),
            background_normal='', 
            background_down='',
            background_color=(0,0,0,0)
        )
        style_round_texture_widget(
            vs_friend_btn,
            image_path=BTN_FRIEND,
            radius=12
        )
        enable_press_darken(vs_friend_btn, factor=0.5)
        enable_click_sound(vs_friend_btn)
        vs_friend_btn.bind(on_release=lambda *_: self.start_game('friend'))

        # --- Thêm nút vào layout ---
        button_container.add_widget(vs_bot_btn)
        button_container.add_widget(vs_friend_btn)
        
        # --- Thêm tất cả vào main_layout ---
        main_layout.add_widget(title)
        main_layout.add_widget(settings_container)
        main_layout.add_widget(button_container)
        
        root.add_widget(main_layout)
        self.add_widget(root)
        self.root_widget = root
        
        # Cập nhật text_size Label khi GridLayout resize
        settings_container.bind(size=self._update_settings_label_text_size)


    # ------------------------------------------------------------------ #
    #                       CẬP NHẬT GIAO DIỆN                           #
    # ------------------------------------------------------------------ #
    def _update_settings_label_text_size(self, widget, value):
        for child in widget.children:
            if isinstance(child, Label):
                child.text_size = (widget.width * 0.4 - 20, None)

    def _update_bg(self, widget, *args):
        self.bg.pos = widget.pos
        self.bg.size = widget.size
    
    # ------------------------------------------------------------------ #
    #                     POPUP CHỌN ĐỘ KHÓ AI                           #
    # ------------------------------------------------------------------ #
    def show_difficulty_popup(self, instance):
        """Hiển thị popup chọn độ khó AI."""
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)
        popup = Popup(
            title='Select Difficulty',
            title_font= FONT_BOLD,
            content=content,
            size_hint=(0.7, 0.4),
            background=SELECT_DIF,
            title_color=(1,1,1,1),
            title_align='center',
            title_size='28sp' 
        )
        
        def create_popup_button(caption: str, diff_level: str) -> Button:
            btn = Button(
                text=caption,
                markup=True,                 
                font_size='20sp',
                size_hint=(1, .3),
                color=(0, 0, 0, .7),          
                background_normal='',        
                background_down='',
                background_color=(0, 0, 0, 0)  
            )

            style_round_button(btn, rgba=(1, 1, 1, .6), radius=10)
            enable_press_darken(btn, factor=0.5)
            enable_click_sound(btn)
            btn.bind(on_release=lambda *_: self.select_difficulty(diff_level, popup))
            return btn

        popup.separator_color = (1, 0.6, 0.2, 1)

        # -------- 3 nút --------
        content.add_widget(create_popup_button('[b]Easy[/b]',   'easy'))
        content.add_widget(create_popup_button('[b]Medium[/b]', 'medium'))
        content.add_widget(create_popup_button('[b]Hard[/b]',   'hard'))

        popup.open()
    
    def select_difficulty(self, difficulty, popup):
        """Handle difficulty selection."""
        popup.dismiss()
        self.start_game('bot', difficulty)
    
    # ------------------------------------------------------------------ #
    #                       KHỞI ĐỘNG VÁN CỜ                             #
    # ------------------------------------------------------------------ #
    def start_game(self, mode, difficulty=None):
        """Start the game with selected mode and custom settings."""
        app = App.get_running_app()
        if app:
            try:
                rows = int(self.rows_input.text)
                cols = int(self.cols_input.text)
                win_len = int(self.win_len_input.text)
                num_obstacles = int(self.num_obstacles_input.text)
            except ValueError:
                self._show_error_popup("Lỗi nhập liệu", "Vui lòng nhập số nguyên hợp lệ cho tất cả các trường.")
                return

            # Kiểm tra giá trị hợp lệ cơ bản
            if rows <= 0 or cols <= 0 or win_len <= 0 or num_obstacles < 0:
                self._show_error_popup("Lỗi giá trị", "Các giá trị phải lớn hơn 0 (trừ số chướng ngại vật có thể là 0).")
                return
            if win_len > rows and win_len > cols:
                self._show_error_popup("Lỗi logic", "Độ dài thắng không thể lớn hơn cả số hàng và số cột.")
                return
            if num_obstacles >= (rows * cols): # Đảm bảo còn ít nhất 1 ô trống để chơi
                 self._show_error_popup("Lỗi logic", "Số chướng ngại vật quá lớn, không đủ ô trống để chơi.")
                 return

            # Truyền các tham số mới này khi bắt đầu game
            app.start_game(mode, difficulty, rows=rows, cols=cols, win_len=win_len, num_obstacles=num_obstacles)

    # ------------------------------------------------------------------ #
    #                           POPUP ERROR                              #
    # ------------------------------------------------------------------ #
    def _show_error_popup(self, title, message):
        # ------ Layout gốc của popup ------
        content = BoxLayout(orientation='vertical',
                            spacing=dp(10),
                            padding=dp(10),
                            size_hint=(1, 1))

        # ------ ScrollView + container ------
        scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)

        # container giữ Label, chỉnh padding để căn giữa
        container = BoxLayout(orientation='vertical',
                            size_hint_y=None,
                            padding=[0, 0, 0, 0])   # L, T, R, B
        container.bind(minimum_height=lambda inst, val: setattr(inst, 'height', val))

        msg_lbl = Label(
            text=f'[b]{message}[/b]',
            markup=True,
            halign='center',
            valign='middle',
            color=(.9, .9, .9, 1),
            size_hint_y=None
        )

        # ———  Wrap + tự điều chỉnh height  ———
        def _update_wrap(instance, width):
            instance.text_size = (width, None)
        msg_lbl.bind(width=_update_wrap)
        msg_lbl.bind(texture_size=lambda inst, ts: setattr(inst, 'height', ts[1]))

        # ———  Hàm căn giữa dọc khi text ngắn  ———
        def _center_vertically(*_):
            avail = scroll.height
            txt_h = msg_lbl.height
            pad = max((avail - txt_h) / 2, 0)
            container.padding = [0, pad, 0, pad]

        # Cập nhật khi cửa sổ hoặc label đổi kích thước
        scroll.bind(height=_center_vertically)
        msg_lbl.bind(height=_center_vertically)

        container.add_widget(msg_lbl)
        scroll.add_widget(container)
        content.add_widget(scroll)

        # ------ Nút OK ------
        close_btn = Button(
            text='[b]OK[/b]',
            markup=True,
            size_hint=(1, None),
            height=dp(40),
            color=(.9, .9, .9, 1)
        )
        style_round_button(close_btn, rgba=(0, 0, 0, .7), radius=10)
        enable_press_darken(close_btn, factor=0.5)
        enable_click_sound(close_btn) 
        content.add_widget(close_btn)

        # ------ Tạo và mở Popup ------
        popup = Popup(
            title=title,
            title_font=FONT_BOLD,
            title_size='24sp',
            title_color=(.8, .8, .8, 1),
            separator_color=(1, 0, 0, 1),
            content=content,
            size_hint=(0.7, 0.3),
            background=BG_ERROR,
            auto_dismiss=False
        )

        close_btn.bind(on_release=popup.dismiss)
        popup.open()

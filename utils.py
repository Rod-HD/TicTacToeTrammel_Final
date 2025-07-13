"""
Tiện ích UI (bo góc, nhấn tối, âm click)
======================================================
Chứa hàm dựng hiệu ứng bo góc cho Kivy widget và phát âm click.
"""
from kivy.graphics import Color, RoundedRectangle
from kivy.core.image import Image as CoreImage
from sound_manager import SoundManager
from sound_manager import SoundManager

# ---------------------- CONSTANT / SINGLETON ----------------------- #
# Trình phát âm thanh dùng chung
# Đề xuất: CLICK_VOLUME và CLICK_SFX có thể cấu hình trong game_config
_CLICKER = SoundManager(auto_play_bg=False)


# ------------------------------------------------------------------ #
#                       ÂM THANH CLICK BUTTON                        #
# ------------------------------------------------------------------ #
def enable_click_sound(widget):
    """Phát click.ogg mỗi khi Button được release."""
    widget.bind(on_release=lambda *_: _CLICKER.play_click())
    
# ------------------------------------------------------------------ #
#                        STYLE: BO GÓC + NỀN                         #
# ------------------------------------------------------------------ #
def style_round_button(btn, rgba, radius=15):
    """Tô màu tròn + bo góc cho Button."""
    btn.canvas.before.clear()
    btn.background_normal = ''
    btn.background_down   = ''
    btn.background_color  = (0, 0, 0, 0)

    with btn.canvas.before:
        clr = Color(*rgba)               
        rect = RoundedRectangle(pos=btn.pos,
                                size=btn.size,
                                radius=[radius])

    # Lưu reference để darken / resize
    btn._bg_clr  = clr
    btn._bg_rect = rect

    def _update(*_):
        rect.pos = btn.pos
        rect.size = btn.size
    btn.bind(pos=_update, size=_update)

def style_round_widget(widget, rgba, radius=15):
    """Bo góc + nền cho mọi widget (không phải Button)."""
    widget.canvas.before.clear()
    
    with widget.canvas.before:
        clr = Color(*rgba)                   
        rect = RoundedRectangle(pos=widget.pos,
                                size=widget.size,
                                radius=[radius])

    widget._bg_clr  = clr                    
    widget._bg_rect = rect

    def _update(*_):
        rect.pos, rect.size = widget.pos, widget.size
    widget.bind(pos=_update, size=_update)

def style_round_texture_widget(widget, image_path, radius=15):
    """Bo góc + dùng texture ảnh làm nền."""
    widget.canvas.before.clear()

    with widget.canvas.before:
        clr = Color(1, 1, 1, 1)                       
        rect = RoundedRectangle(
            pos=widget.pos, size=widget.size,
            radius=[radius],
            texture=CoreImage(image_path).texture     
        )

    widget._bg_clr  = clr
    widget._bg_rect = rect

    widget.bind(pos=lambda inst, _: setattr(rect, 'pos', inst.pos),
                size=lambda inst, _: setattr(rect, 'size', inst.size))
    
# ------------------------------------------------------------------ #
#                      HIỆU ỨNG NHẤN TỐI (DARKEN)                    #
# ------------------------------------------------------------------ #
def enable_press_darken(widget, factor=0.5):
    """State 'down' -> overlay tối hơn *factor* (0=đen hoàn toàn)."""
    if not hasattr(widget, "_bg_clr"):
        raise AttributeError("Widget chưa có _bg_clr; hãy áp dụng style_round_* trước!")

    orig_rgba = widget._bg_clr.rgba

    def _press(inst, new_state):
        inst._bg_clr.rgba = (factor, factor, factor, 1) if new_state == 'down' else orig_rgba

    widget.bind(state=_press)
    
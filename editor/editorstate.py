import pyray

from engine import metrics as m
from engine.state import state
from engine.widget import label
from editor import editorlevel
from engine.windows import window, windowmanager
from utils import tiledbackground
from widgets import valuelabel
import globalresources as res


def make_info_window(editor_state):
    level: editorlevel.EditorLevel = editor_state.level

    win = window.Window(40, 40, 300, 150)
    win.title = "Level info"
    win.background_color = (20, 20, 20, 255)

    # Level width
    win.add_widget(label.Label(5, 5, "TL", "Level width (tile) :", 10))
    win.add_widget(valuelabel.ValueLabel(120, 5, "TL", level.level_horizontal_tiles, 10))

    # Level height
    win.add_widget(label.Label(5, 15, "TL", "Level height (tile) :", 10))
    win.add_widget(valuelabel.ValueLabel(120, 15, "TL", level.level_vertical_tiles, 10))

    # Tile width
    win.add_widget(label.Label(5, 25, "TL", "Tile width :", 10))
    win.add_widget(valuelabel.ValueLabel(120, 25, "TL", level.tile_width, 10))

    # Tile height
    win.add_widget(label.Label(5, 35, "TL", "Tile height :", 10))
    win.add_widget(valuelabel.ValueLabel(120, 35, "TL", level.tile_height, 10))

    # Level width (meters)
    win.add_widget(label.Label(5, 45, "TL", "Level width (meter) :", 10))
    win.add_widget(valuelabel.ValueLabel(120, 45, "TL", level.level_width_meter, 10))

    # Level height (meters)
    win.add_widget(label.Label(5, 55, "TL", "Level height (meter) :", 10))
    win.add_widget(valuelabel.ValueLabel(120, 55, "TL", level.level_height_meter, 10))

    return win


class EditorState(state.State):
    def __init__(self):
        super().__init__()
        m.set_camera_center(pyray.Vector2(0.0, 0.0))

        self.window_manager = windowmanager.WindowManager()
        self.level = editorlevel.EditorLevel()

        self.bg = tiledbackground.TiledBackground(res.menu_bg_grayscale_sprite, color=(20, 20, 20, 255))
        self.window_manager.add_window(make_info_window(self))

    def update(self, dt: float):
        self.bg.update(dt)
        self.window_manager.update(dt)

    def draw(self):
        self.bg.draw()
        self.window_manager.draw()

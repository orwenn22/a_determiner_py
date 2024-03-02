import pyray
from engine.state import state
from engine.widget import widgetmanager, label
from widgets import previewbutton
import os
import gameplaystate
from engine import globals as g
import globalresources as res


class ChoiceLevelState(state.State):
    def __init__(self):
        super().__init__()

        self.list_level_file: list[str] = os.listdir("maps/")
        self.list_preview: list[pyray.Texture] = []
        self.widget_manager = widgetmanager.WidgetManager()

        # Title (static)
        title = label.Label(0, 0, "TC", "Choose the level", 30).set_scrollable(False)
        self.widget_manager.add_widget(title)

        # Level buttons (scrollable)
        for i in range(len(self.list_level_file)):
            if self.list_level_file[i][:-4] + "_preview.png" in os.listdir("preview/"):
                self.list_preview.append(pyray.load_texture("preview/" + self.list_level_file[i][:-4] + "_preview.png"))
            else:
                self.list_preview.append(pyray.load_texture("res/default.png"))     # loading the preview

            level_button = previewbutton.PreviewButton(0, i*120, 300, 100, "MC",
                                                       res.tiled_button_sprite, 8, self.list_preview[i], 1,
                                                       self.list_level_file[i][:-4], act=self.make_play_action(i))
            level_button.set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
            self.widget_manager.add_widget(level_button)

        self.widget_manager.set_scrolling_proportions(0, 0, -len(self.list_level_file)*120, 0)
        self.widget_manager.set_scrolling_flags(False, True)
        # TODO: maybe change the background to something like in the other parts of the menu

    def unload_ressources(self):
        for i in self.list_preview:
            pyray.unload_texture(i)

    def update(self, dt):
        self.widget_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()

    def make_play_action(self, map_number: int = 0):
        def local_play_action():
            self.manager.set_state(gameplaystate.GameplayState.from_level_file(self.list_level_file[map_number]))
        return local_play_action


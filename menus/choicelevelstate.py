import pyray
from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton
from widgets import previewbutton
import os
import gameplaystate
from utils import tiledbackground
import globalresources as res
from menus import menustate


class ChoiceLevelState(state.State):
    def __init__(self):
        super().__init__()
        self.widget_manager = widgetmanager.WidgetManager()
        self.list_preview: list[pyray.Texture] = []

        # For checkerboard background
        self.bg = tiledbackground.TiledBackground(res.menu_bg_sprite)

        def back_to_main_menu():
            main_menu = menustate.MenuState()
            main_menu.bg.set_scrolling(self.bg.scrolling.x, self.bg.scrolling.y)
            self.manager.set_state(main_menu)

        # Add back to main menu button
        back_button = tiledbutton.TiledButton(0, 10, 110, 40, "TL",
                                              res.tiled_button_right_sprite, 8, 2,                                                  "Back", back_to_main_menu)
        back_button.set_scrollable(False).center_text().set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
        self.widget_manager.add_widget(back_button)

        if "maps" not in os.listdir("./"):
            self.widget_manager.add_widget(label.Label(0, 0, "MC", "No maps folder :(", 20, pyray.RED))
            return

        # Load the map list
        self.list_level_file: list[str] = os.listdir("maps/")

        # Title (static)
        title = label.Label(0, 10, "TC", "Choose the level", 30, pyray.BLACK).set_scrollable(False)
        self.widget_manager.add_widget(title)

        # Level buttons (scrollable)
        for i in range(len(self.list_level_file)):
            level_name = self.list_level_file[i][:-4]       # TODO : function to cleanly remove the extension ?

            if "preview" not in os.listdir("./") or level_name + "_preview.png" not in os.listdir("preview/"):
                self.list_preview.append(pyray.load_texture("res/default.png"))  # loading the default preview
            else:
                self.list_preview.append(pyray.load_texture("preview/" + level_name + "_preview.png"))

            # Make and add the actual level entry in the menu
            level_button = previewbutton.PreviewButton(0, i*120, 300, 100, "MC",
                                                       res.tiled_button_sprite, 8, self.list_preview[i], 1,
                                                       level_name, act=self.make_play_action(i))
            level_button.set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
            self.widget_manager.add_widget(level_button)

        # Configure scrolling on the widget manager
        self.widget_manager.set_scrolling_proportions(0, 0, -len(self.list_level_file)*120, 0)
        self.widget_manager.set_scrolling_flags(False, True)

    def unload_ressources(self):
        for i in self.list_preview:
            pyray.unload_texture(i)

    def update(self, dt):
        self.bg.update(dt)
        self.widget_manager.update(dt)

    def draw(self):
        self.bg.draw()
        self.widget_manager.draw()

    def make_play_action(self, map_number: int = 0):
        def local_play_action():
            self.manager.set_state(gameplaystate.GameplayState.from_level_file(self.list_level_file[map_number]))
        return local_play_action


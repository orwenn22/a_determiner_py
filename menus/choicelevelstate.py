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
        self.error_message: None | label.Label = None
        self.list_preview: list[pyray.Texture] = []

        # For checkerboard background
        self.bg = tiledbackground.TiledBackground(res.menu_bg_sprite)

        def back_to_main_menu():
            main_menu = menustate.MenuState()
            main_menu.bg.set_scrolling(self.bg.scrolling.x, self.bg.scrolling.y)
            self.manager.set_state(main_menu)

        # Add back to main menu button
        back_button = tiledbutton.TiledButton(0, 10, 110, 40, "TL",
                                              res.tiled_button_right_sprite, 8, 2,
                                              "Back", back_to_main_menu)
        back_button.set_scrollable(False).center_text().set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
        self.widget_manager.add_widget(back_button)

        if "maps" not in os.listdir("./"):
            self.widget_manager.add_widget(label.Label(0, 0, "MC", "No maps folder :(", 20, pyray.RED))
            return

        # Load the map list
        self.level_files_list: list[str] = os.listdir("maps/")

        # Title (static)
        title = label.Label(0, 10, "TC", "Select the level", 30, pyray.WHITE).set_scrollable(False).set_outline(True)
        self.widget_manager.add_widget(title)

        # Level buttons (scrollable)
        level_count = 0
        for i in range(len(self.level_files_list)):
            if self.level_files_list[i][-4:] not in {".txt", ".lvl"}:
                continue

            level_name = self.level_files_list[i][:-4]       # TODO : function to cleanly remove the extension ?

            if "preview" not in os.listdir("./") or level_name + "_preview.png" not in os.listdir("preview/"):
                self.list_preview.append(pyray.load_texture("res/default.png"))  # loading the default preview
            else:
                self.list_preview.append(pyray.load_texture("preview/" + level_name + "_preview.png"))

            # Make and add the actual level entry in the menu
            level_button = previewbutton.PreviewButton(0, level_count*120, 300, 100, "MC",
                                                       res.tiled_button_sprite, 8, self.list_preview[-1], 1,
                                                       level_name, act=self.make_play_action(i))
            level_button.set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
            self.widget_manager.add_widget(level_button)
            level_count += 1

        # Configure scrolling on the widget manager
        self.widget_manager.set_scrolling_proportions(0, 0, -(level_count-1)*120, 0)
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

    def set_error_message(self, message: str):
        if self.error_message is not None:
            self.widget_manager.remove_widget(self.error_message)
        self.error_message = label.Label(0, 42, "TC", message, 20, (190, 0, 0, 255)).set_scrollable(False)
        self.widget_manager.add_widget(self.error_message)

    def make_play_action(self, map_number: int = 0):
        def local_play_action():
            gameplay_state = gameplaystate.GameplayState.from_level_file(self.level_files_list[map_number])
            if gameplay_state is None:
                self.set_error_message("Error loading level, see console for more info")        # TODO : in the future pass the actual error
                return
            self.manager.set_state(gameplay_state)
        return local_play_action


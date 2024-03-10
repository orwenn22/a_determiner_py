import pyray
from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton
from widgets import previewbutton
import os
import gameplaystate
from engine import globals as g
import globalresources as res
from menus import menustate


class ChoiceLevelState(state.State):
    def __init__(self):
        super().__init__()

        def back_to_main_menu():
            main_menu = menustate.MenuState()
            main_menu.bg_rect.x = self.bg_rect.x
            main_menu.bg_rect.y = self.bg_rect.y
            self.manager.set_state(main_menu)

        # Load the map list
        self.list_level_file: list[str] = os.listdir("maps/")
        self.list_preview: list[pyray.Texture] = []
        self.widget_manager = widgetmanager.WidgetManager()

        # Title (static)
        title = label.Label(0, 10, "TC", "Choose the level", 30, pyray.BLACK).set_scrollable(False)
        self.widget_manager.add_widget(title)

        # Level buttons (scrollable)
        for i in range(len(self.list_level_file)):
            level_name = self.list_level_file[i][:-4]       # TODO : function to cleanly remove the extension ?
            if level_name + "_preview.png" in os.listdir("preview/"):
                self.list_preview.append(pyray.load_texture("preview/" + level_name + "_preview.png"))
            else:
                self.list_preview.append(pyray.load_texture("res/default.png"))     # loading the default preview

            # Make and add the actual level entry in the menu
            level_button = previewbutton.PreviewButton(0, i*120, 300, 100, "MC",
                                                       res.tiled_button_sprite, 8, self.list_preview[i], 1,
                                                       level_name, act=self.make_play_action(i))
            level_button.set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
            self.widget_manager.add_widget(level_button)

        # Configure scrolling on the widget manager
        self.widget_manager.set_scrolling_proportions(0, 0, -len(self.list_level_file)*120, 0)
        self.widget_manager.set_scrolling_flags(False, True)

        # Add back to main menu button
        back_button = tiledbutton.TiledButton(0, 10, 110, 40, "TL",
                                              res.tiled_button_right_sprite, 8, 2,
                                              "Back", back_to_main_menu)
        back_button.set_scrollable(False).center_text().set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
        self.widget_manager.add_widget(back_button)

        # For checkerboard background
        self.bg_rect = pyray.Rectangle(0, 0, res.menu_bg_sprite.width, res.menu_bg_sprite.height)

    def unload_ressources(self):
        for i in self.list_preview:
            pyray.unload_texture(i)

    def update(self, dt):
        self.bg_rect.x += 12 * dt
        self.bg_rect.y += 12 * dt
        self.widget_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        for y in range(0, pyray.get_render_height(), res.menu_bg_sprite.height):
            for x in range(0, pyray.get_render_width(), res.menu_bg_sprite.width):
                pyray.draw_texture_rec(res.menu_bg_sprite, self.bg_rect, pyray.Vector2(x, y), pyray.WHITE)
        self.widget_manager.draw()

    def make_play_action(self, map_number: int = 0):
        def local_play_action():
            self.manager.set_state(gameplaystate.GameplayState.from_level_file(self.list_level_file[map_number]))
        return local_play_action

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

        # the next two variables are only there to detect if we should be able to scroll or no
        self.top_button_y = 50
        self.down_button_y = self.top_button_y + len(self.list_level_file)*120*5

        # Title (static)
        self.title_widget_manager = widgetmanager.WidgetManager()
        title = label.Label(0, 0, "TC", "Choose the level", 30)
        self.title_widget_manager.add_widget(title)

        # Level buttons (scrollable)
        self.widget_manager = widgetmanager.WidgetManager()
        for i in range(len(self.list_level_file)):
            if self.list_level_file[i][:-4] + "_preview.png" in os.listdir("preview/"):
                self.list_preview.append(pyray.load_texture("preview/" + self.list_level_file[i][:-4] + "_preview.png"))
            else:
                self.list_preview.append(pyray.load_texture("res/default.png"))     # loading the preview

            level_button = previewbutton.PreviewButton(0, self.top_button_y + i*120, 300, 100, "TC",
                                                       res.tiled_button_sprite, 8, self.list_preview[i], 1,
                                                       self.list_level_file[i][:-4], act=self.make_play_action(i))
            level_button.set_hovering_color(pyray.YELLOW).set_font_color(pyray.WHITE)
            self.widget_manager.add_widget(level_button)
    
        #TODO: maybe change the background to something like in the other parts of the menu

    def unload_ressources(self):
        for i in self.list_preview:
            pyray.unload_texture(i)

    def update(self, dt):
        self.widget_manager.update(dt)
        if g.mouse_wheel < 0 and self.down_button_y > pyray.get_screen_height():
            self.top_button_y -= 120
            self.down_button_y -= 120
            for i in self.widget_manager.list_widget:
                i.coordinate.y -= 120
        if g.mouse_wheel > 0 and self.top_button_y < 20:
            self.top_button_y += 120
            self.down_button_y += 120
            for i in self.widget_manager.list_widget:
                i.coordinate.y += 120
        self.title_widget_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()
        self.title_widget_manager.draw()

    def make_play_action(self, map_number: int = 0):
        def local_play_action():
            self.manager.set_state(gameplaystate.GameplayState(self.list_level_file[map_number]))
        return local_play_action


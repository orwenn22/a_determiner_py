import pyray

from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton
from engine import globals as g
from menus import menustate
import globalresources as res


class PauseMenu(state.State):
    def __init__(self, gameplay_state):
        import gameplaystate
        super().__init__()
        self.gameplay_state: gameplaystate.GameplayState = gameplay_state       # TODO : handle any type of state ?
        self.widget_manager = widgetmanager.WidgetManager()

        self.widget_manager.add_widget(label.Label(0, -55, "MC", "== PAUSE ==", 20, pyray.WHITE))

        def local_resume():
            self._resume()
        self.widget_manager.add_widget(
            tiledbutton.TiledButton(0, -10, 150, 40, "MC",
                                    res.tiled_button_sprite, 8, 2,
                                    "Resume",
                                    local_resume
                                    ).center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)
        )

        def back_to_main_menu():
            self.manager.set_state(menustate.MenuState())
        self.widget_manager.add_widget(
            tiledbutton.TiledButton(0, 40, 150, 40, "MC",
                                    res.tiled_button_sprite, 8, 2,
                                    "Main menu",
                                    back_to_main_menu
                                    ).center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.RED)
        )

    # If the user quit using the cross of the window or if we go back to the main menu, we need to unload the map
    def unload_ressources(self):
        if self.gameplay_state is not None:
            self.gameplay_state.unload_ressources()

    def update(self, dt: float):
        if g.is_key_pressed(pyray.KeyboardKey.KEY_ESCAPE):
            self._resume()
            return

        self.widget_manager.update(dt)
        g.mouse_used = True

        # Make sure we reposition the UI of the gameplay if the window is resized
        if self.gameplay_state is not None:
            self.gameplay_state.overlay.update(dt)
            self.gameplay_state.actions_widgets.update(dt)
            self.gameplay_state.window_manager.update(dt)

    def draw(self):
        self.gameplay_state.draw()
        pyray.draw_rectangle(0, 0, pyray.get_screen_width(), pyray.get_screen_height(), (0, 0, 0, 100))
        self.widget_manager.draw()

    def _resume(self):
        self.manager.set_state(self.gameplay_state)
        self.gameplay_state = None      # Do this so we don't unload the resources

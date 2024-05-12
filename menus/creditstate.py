import pyray
from engine.state import state
from engine.widget import tiledbutton, widgetmanager, label
from utils import tiledbackground
import globalresources as res


class CreditState(state.State):
    def __init__(self):
        from menus import menustate
        super().__init__()

        def return_action():
            self.manager.set_state(menustate.MenuState())

        self.widget_manager = widgetmanager.WidgetManager()

        title = label.Label(0, -150, "MC", "À déterminer", 40, pyray.WHITE).set_outline(True)
        tm = label.Label(140, -160, "MC", "TM", 10, pyray.WHITE).set_outline(True)
        group = label.Label(0, -100, "MC", "By : SomeGroup", 30, pyray.WHITE).set_outline(True)

        return_to_menu = tiledbutton.TiledButton(0, 200, 250, 40, "MC",
                                                 res.tiled_button_sprite, 8, 2,
                                                 "Return to main menu", return_action)
        return_to_menu.center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        self.widget_manager.add_widget(title)
        self.widget_manager.add_widget(tm)
        self.widget_manager.add_widget(group)
        self.widget_manager.add_widget(label.Label(0, -60, "MC", "Ewenn Baudet", 20, pyray.WHITE).set_outline(True))
        self.widget_manager.add_widget(label.Label(0, -30, "MC", "Alexis Delavis", 20, pyray.WHITE).set_outline(True))
        self.widget_manager.add_widget(label.Label(0, 0, "MC", "Jude Aybalen", 20, pyray.WHITE).set_outline(True))
        self.widget_manager.add_widget(label.Label(0, 30, "MC", "Adrian Noyes", 20, pyray.WHITE).set_outline(True))
        self.widget_manager.add_widget(label.Label(0, 60, "MC", "Maxime Duret", 20, pyray.WHITE).set_outline(True))
        self.widget_manager.add_widget(return_to_menu)

        self.bg = tiledbackground.TiledBackground(res.menu_bg_credits_sprite)

    def update(self, dt):
        self.bg.update(dt)
        self.widget_manager.update(dt)

    def draw(self):
        self.bg.draw()
        self.widget_manager.draw()

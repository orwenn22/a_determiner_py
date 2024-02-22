import pyray
from engine.state import state
from engine.widget import button, widgetmanager, label
import globalresources as res


class CreditState(state.State):
    def __init__(self):
        from menus import menustate
        super().__init__()

        def return_action():
            self.manager.set_state(menustate.MenuState())

        self.widget_manager = widgetmanager.WidgetManager()

        title = label.Label(0, -150, "MC", "À déterminer", 40, pyray.WHITE)
        tm = label.Label(140, -160, "MC", "TM", 10, pyray.WHITE)
        group = label.Label(0, -100, "MC", "By : SomeGroup", 30, pyray.WHITE)

        return_to_menu = button.Button(0, 200, 250, 40, "MC", return_action, "Return to main menu")

        self.widget_manager.add_widget(title)
        self.widget_manager.add_widget(tm)
        self.widget_manager.add_widget(group)
        self.widget_manager.add_widget(label.Label(0, -60, "MC", "Ewenn Baudet", 20, pyray.WHITE))
        self.widget_manager.add_widget(label.Label(0, -30, "MC", "Alexis Delavis", 20, pyray.WHITE))
        self.widget_manager.add_widget(label.Label(0, 0, "MC", "Jude Aybalen", 20, pyray.WHITE))
        self.widget_manager.add_widget(label.Label(0, 30, "MC", "Adrian Noyes", 20, pyray.WHITE))
        self.widget_manager.add_widget(label.Label(0, 60, "MC", "Maxime Duret", 20, pyray.WHITE))
        self.widget_manager.add_widget(return_to_menu)

        self.bg_rect = pyray.Rectangle(0, 0, res.menu_bg_credits_sprite.width, res.menu_bg_credits_sprite.height)

    def update(self, dt):
        self.bg_rect.x += 12 * dt
        self.bg_rect.y += 12 * dt
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        for y in range(0, pyray.get_render_height(), res.menu_bg_sprite.height):
            for x in range(0, pyray.get_render_width(), res.menu_bg_sprite.width):
                pyray.draw_texture_rec(res.menu_bg_credits_sprite, self.bg_rect, pyray.Vector2(x, y), pyray.WHITE)
        self.widget_manager.draw()

import pyray
from engine import globals as g
from engine.state import state
from engine.widget import button, widgetmanager, label
import globalresources as res


class MenuState(state.State):
    def __init__(self):
        import gameplaystate
        from menus import optionstate, creditstate
        super().__init__()

        def play_action():
            self.manager.set_state(gameplaystate.GameplayState())

        def options_action():
            self.manager.set_state(optionstate.OptionState())

        def credits_action():
            self.manager.set_state(creditstate.CreditState())

        def quit_action():
            g.running = False

        self.widget_manager = widgetmanager.WidgetManager()

        play_button = button.Button(0, -100, 150, 40, "MC", play_action, "Play Game")
        options_button = button.Button(0, -50, 150, 40, "MC", options_action, "Options")
        credits_button = button.Button(0, 0, 150, 40, "MC", credits_action, "Credits")
        quit_button = button.Button(0, 50, 150, 40, "MC", quit_action, "Quit")

        title = label.Label(0, -200, "MC", "À déterminer", 40, pyray.Color(0, 0, 0, 255))
        tm = label.Label(140, -210, "MC", "TM", 10, pyray.Color(0, 0, 0, 255))

        self.widget_manager.add_widget(play_button)
        self.widget_manager.add_widget(options_button)
        self.widget_manager.add_widget(credits_button)
        self.widget_manager.add_widget(quit_button)
        self.widget_manager.add_widget(title)
        self.widget_manager.add_widget(tm)

        self.bg_rect = pyray.Rectangle(0, 0, res.menu_bg_sprite.width, res.menu_bg_sprite.height)

    def update(self, dt):
        self.bg_rect.x += 12*dt
        self.bg_rect.y += 12*dt
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        for y in range(0, pyray.get_render_height(), res.menu_bg_sprite.height):
            for x in range(0, pyray.get_render_width(), res.menu_bg_sprite.width):
                pyray.draw_texture_rec(res.menu_bg_sprite, self.bg_rect, pyray.Vector2(x, y), pyray.WHITE)
        self.widget_manager.draw()

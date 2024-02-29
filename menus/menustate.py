import pyray
from engine import globals as g
from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton
import globalresources as res


class MenuState(state.State):
    def __init__(self):
        import gameplaystate
        from menus import optionstate, creditstate, transitionstate, choicelevelstate
        super().__init__()

        def play_action():
            #self.manager.set_state(gameplaystate.GameplayState())
            self.manager.set_state(choicelevelstate.ChoiceLevelState())

        def options_action():
            self.manager.set_state(optionstate.OptionState())

        def credits_action():
            # self.manager.set_state(creditstate.CreditState())
            self.manager.set_state(transitionstate.TransitonState(self, creditstate.CreditState()))

        def quit_action():
            g.running = False

        self.widget_manager = widgetmanager.WidgetManager()

        title = label.Label(0, -150, "MC", "À déterminer", 40, pyray.Color(0, 0, 0, 255))
        tm = label.Label(140, -160, "MC", "TM", 10, pyray.Color(0, 0, 0, 255))

        play_button = tiledbutton.TiledButton(0, -50, 150, 40, "MC",
                                              res.tiled_button_sprite, 8, 2,
                                              "Play Game", play_action).center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        options_button = tiledbutton.TiledButton(0, 0, 150, 40, "MC",
                                                 res.tiled_button_sprite, 8, 2,
                                                 "Options", options_action).center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        credits_button = tiledbutton.TiledButton(0, 50, 150, 40, "MC",
                                                 res.tiled_button_sprite, 8, 2,
                                                 "Credits", credits_action).center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        quit_button = tiledbutton.TiledButton(0, 100, 150, 40, "MC",
                                              res.tiled_button_sprite, 8, 2,
                                              "Quit", quit_action).center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.RED)

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
        self.widget_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        for y in range(0, pyray.get_render_height(), res.menu_bg_sprite.height):
            for x in range(0, pyray.get_render_width(), res.menu_bg_sprite.width):
                pyray.draw_texture_rec(res.menu_bg_sprite, self.bg_rect, pyray.Vector2(x, y), pyray.WHITE)
        self.widget_manager.draw()

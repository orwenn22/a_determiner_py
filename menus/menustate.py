import pyray
import random
from engine import globals as g
from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton
from utils import tiledbackground, keyboardcode
import globalresources as res
import gameplaystate


class MenuState(state.State):
    def __init__(self):
        from menus import optionstate, creditstate, transitionstate, choicelevelstate
        super().__init__()

        def play_action():
            choice_level_state = choicelevelstate.ChoiceLevelState()
            choice_level_state.bg.set_scrolling(self.bg.scrolling.x, self.bg.scrolling.y)   # Make sure the background is kept in sync
            self.manager.set_state(choice_level_state)

        def options_action():
            self.manager.set_state(optionstate.OptionState())

        def credits_action():
            # self.manager.set_state(creditstate.CreditState())
            self.manager.set_state(transitionstate.TransitonState(self, creditstate.CreditState()))

        def quit_action():
            g.running = False

        self.widget_manager = widgetmanager.WidgetManager()

        title = label.Label(0, -150, "MC", "À déterminer", 40, pyray.Color(255, 255, 255, 255))
        title.enable_outline = True
        title.outline_color = pyray.BLACK

        tm = label.Label(140, -160, "MC", "TM", 10, pyray.Color(255, 255, 255, 255))
        tm.enable_outline = True
        tm.outline_color = pyray.BLACK

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
        self.code = keyboardcode.KeyboardCode("SILLY", self.silly)
        self.bg = tiledbackground.TiledBackground(res.menu_bg_sprite)

    def update(self, dt):
        self.bg.update(dt)
        self.widget_manager.update(dt)
        self.code.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.bg.draw()
        self.widget_manager.draw()

    def silly(self):
        gameplay_state = None
        if random.randint(0, 100) < 90:
            gameplay_state = gameplaystate.GameplayState.from_level_file("old/silly.txt")
        else:
            gameplay_state = gameplaystate.GameplayState.from_level_file("old/silly_better.txt")
        if gameplay_state is not None:
            self.manager.set_state(gameplay_state)

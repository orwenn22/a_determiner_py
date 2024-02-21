import pyray
from engine import globals as g
from engine.state import state
from engine.widget import button, widgetmanager, label
import gameplaystate
import optionstate
import creditstate


class MenuState(state.State):
    def __init__(self):
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

        title = label.Label(0, -200, "MC", "À déterminer", 40, pyray.Color(127, 127, 127, 255))
        tm = label.Label(140, -210, "MC", "TM", 10, pyray.Color(127, 127, 127, 255))

        self.widget_manager.add_widget(play_button)
        self.widget_manager.add_widget(options_button)
        self.widget_manager.add_widget(credits_button)
        self.widget_manager.add_widget(quit_button)
        self.widget_manager.add_widget(title)
        self.widget_manager.add_widget(tm)

    def update(self, dt):
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()

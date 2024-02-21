import pyray
from engine.state import state
from engine.widget import button, widgetmanager
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
            # TODO : unload state_manager from here or juste add a condition in the main loop
            self.manager.unload()
            pyray.close_window()

        self.widget_manager = widgetmanager.WidgetManager()

        self.play = button.Button(0, -100, 150, 40, "MC", play_action, "Play Game")
        self.options = button.Button(0, -50, 150, 40, "MC", options_action, "Options")
        self.credits = button.Button(0, 0, 150, 40, "MC", credits_action, "Credits")
        self.quit = button.Button(0, 50, 150, 40, "MC", quit_action, "Quit")

        self.title = button.Button(-50, -200, 250, 80, "MC", label="À déterminer tm")
        self.title.set_font_size(40).set_color(pyray.Color(0, 0, 0, 0)).set_font_color(pyray.Color(127, 127, 127, 255))

        self.widget_manager.add_widget(self.play)
        self.widget_manager.add_widget(self.options)
        self.widget_manager.add_widget(self.credits)
        self.widget_manager.add_widget(self.quit)
        self.widget_manager.add_widget(self.title)

    def update(self, dt):
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()

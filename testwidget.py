from engine.state import state
from engine.widget import button
from engine.widget import widgetmanager
import pyray
import engine.globals as g


def testfunc_builder(text: str):
    def local_testfunc():
        print(text)
    return local_testfunc


class WidgetTest(state.State):
    def __init__(self):
        super().__init__()

        self.widget_manager = widgetmanager.WidgetManager()

        self.widget_manager.add_widget(button.Button(
            10, 10, 100, 100, "TL",
            pyray.Color(100, 100, 100, 255), testfunc_builder("Top left"), "ClickMe"))

        self.widget_manager.add_widget(button.Button(
            0, 0, 100, 100, "MC",
            pyray.Color(100, 100, 100, 255), testfunc_builder("Middle center"), "ClickMe"))

        self.widget_manager.add_widget(button.Button(
            10, 10, 100, 100, "BR",
            pyray.Color(100, 100, 100, 255), testfunc_builder("Bottom right"), "ClickMe"))

    def update(self, dt):
        if g.is_key_pressed(pyray.KeyboardKey.KEY_T):
            import gameplaystate
            self.manager.set_state(gameplaystate.GameplayState())
            return
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        self.widget_manager.draw()

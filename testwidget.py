from engine.state import state
from engine.widget import widget_objects
from engine.widget import widgetmanager
import pyray
import engine.globals as g


def testfunc():
    print("Button clicked")


class WidgetTest(state.State):
    def __init__(self):
        super().__init__()

        self.widget_manager = widgetmanager.WidgetManager()
        self.widget_manager.add_widget(widget_objects.Widget(
            10, 10, 100, 100, pyray.Color(100, 100, 100, 255), "TL", testfunc, "ClickMe"))

    def update(self, dt):
        if g.is_key_pressed(pyray.KeyboardKey.KEY_T):
            import gameplaystate
            self.manager.set_state(gameplaystate.GameplayState())
            return
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        self.widget_manager.draw()

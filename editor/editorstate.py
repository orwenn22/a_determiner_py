import pyray

from engine.state import state
from engine.widget import button as button
from editor import editorwindow, windowmanager


def make_window():
    win = editorwindow.EditorWindow(40, 40, 300, 150)
    win.add_widget(button.Button(3, 3, 60, 30, "TL", label="wow"))
    win.add_widget(button.Button(3, 3, 60, 30, "BR", label="wow"))
    return win


class EditorState(state.State):
    def __init__(self):
        super().__init__()

        self.window_manager = windowmanager.WindowManager()
        self.window_manager.add_window(make_window())
        self.window_manager.add_window(make_window())
        self.window_manager.add_window(make_window())
        self.window_manager.add_window(make_window())

    def update(self, dt: float):
        self.window_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.window_manager.draw()

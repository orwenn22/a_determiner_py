import pyray
from . import widget_objects as w


class WidgetManager():
    def __init__(self):
        self.windows: tuple[int, int] = (pyray.get_screen_width(), pyray.get_screen_height())
        self.list_widget: list[w.Widget] = []

    def update(self):
        if pyray.is_window_resized():
            width_difference = pyray.get_screen_width()/self.windows[0]
            height_difference = pyray.get_screen_height()/self.windows[1]
            self.windows = (pyray.get_screen_width(), pyray.get_screen_height())
            for i in self.list_widget:
                i.reload_size(width_difference, height_difference)
        self.check_pressed()

    def draw(self):
        for i in self.list_widget:
            i.draw()

    def check_pressed(self):
        for i in self.list_widget:
            i.checking_pressed()

    def add_widget(self, widget_to_add: w.Widget):
        self.list_widget.append(widget_to_add)

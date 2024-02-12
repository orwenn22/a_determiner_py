import pyray
from . import button as w


class WidgetManager(object):
    def __init__(self):
        self.list_widget: list[w.Button] = []

    def update(self):
        if pyray.is_window_resized():
            for i in self.list_widget:
                i.reload_placement()

        for i in self.list_widget:
            i.update()

    def draw(self):
        for i in self.list_widget:
            i.draw()

    def add_widget(self, widget_to_add: w.Button):
        self.list_widget.append(widget_to_add)

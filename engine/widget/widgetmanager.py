import pyray
from . import widget_objects as w


class WidgetManager():
    def __init__(self):
        self.list_widget: list[w.Widget] = []

    def update(self):
        if pyray.is_window_resized():
            for i in self.list_widget:
                i.reload_placement()
        self.check_pressed()

    def draw(self):
        for i in self.list_widget:
            i.draw()

    def check_pressed(self):
        for i in self.list_widget:
            i.checking_pressed()

    def add_widget(self, widget_to_add: w.Widget):
        self.list_widget.append(widget_to_add)

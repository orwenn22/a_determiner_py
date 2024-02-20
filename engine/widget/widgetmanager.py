import pyray
from . import widget as w


class WidgetManager(object):
    def __init__(self):
        self.list_widget: list[w.Widget] = []

    def update(self):
        if pyray.is_window_resized():
            for i in self.list_widget:
                i.reload_placement()

        i = 0
        while i < len(self.list_widget):
            self.list_widget[i].update()
            i += 1

    def draw(self):
        for i in self.list_widget:
            i.draw()

    def add_widget(self, widget_to_add: w.Widget):
        self.list_widget.append(widget_to_add)

    def remove_widget(self, widget_to_remove: w.Widget):
        if widget_to_remove not in self.list_widget:
            return
        self.list_widget.remove(widget_to_remove)

    def clear(self):
        self.list_widget.clear()

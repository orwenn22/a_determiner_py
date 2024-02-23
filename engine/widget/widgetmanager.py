import pyray
from . import widget as w


class WidgetManager(object):
    def __init__(self):
        self.list_widget: list[w.Widget] = []
        self.width = pyray.get_render_width()
        self.heigth = pyray.get_render_height()

    def update(self):
        if self.width != pyray.get_render_width() or self.heigth != pyray.get_render_height():
            self.width = pyray.get_render_width()
            self.heigth = pyray.get_render_width()
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

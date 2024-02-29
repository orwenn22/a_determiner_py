import pyray
from . import widget as w
from .. import globals as g


class WidgetManager(object):
    def __init__(self):
        self.list_widget: list[w.Widget] = []

        # TODO : custom WidgetManager position & size to make it more flexible and embeddable everywhere
        self.width = pyray.get_render_width()
        self.height = pyray.get_render_height()

        # Determine if scrolling is enabled or disabled (disabled by default)
        self.enable_h_scrolling = False
        self.enable_v_scrolling = False

        # This is the offset of the scrolling
        self.h_scrolling_offset = 0.0
        self.v_scrolling_offset = 0.0

        # Minimum and maximum scrolling positions
        self.h_scrolling_min = 0.0
        self.h_scrolling_max = 0.0
        self.v_scrolling_min = -100.0
        self.v_scrolling_max = 0.0

        # This is used for the scrolling animation
        self.h_remaining_distance = 0.0
        self.v_remaining_distance = 0.0

        # Indicate if scrolling occurred during this frame
        self.scrolled = False

    def update(self, dt: float):
        # Window resized
        if self.width != pyray.get_render_width() or self.height != pyray.get_render_height():
            self.width = pyray.get_render_width()
            self.height = pyray.get_render_width()
            for i in self.list_widget:
                i.reload_placement()

        # Scrolling
        self.scrolled = False
        if self.enable_h_scrolling:
            self._handle_horizontal_scrolling(dt)
        if self.enable_v_scrolling:
            self._handle_vertical_scrolling(dt)

        if self.scrolled:
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
        widget_to_add.manager = self
        widget_to_add.reload_placement()

    def remove_widget(self, widget_to_remove: w.Widget):
        if widget_to_remove not in self.list_widget:
            return
        self.list_widget.remove(widget_to_remove)

    def clear(self):
        self.list_widget.clear()

    def _handle_horizontal_scrolling(self, dt: float):
        # TODO : process input

        if self.h_remaining_distance == 0:
            return

        self.scrolled = True
        # distance_this_frame = self.h_remaining_distance * (9/10) * dt*10
        distance_this_frame = self.h_remaining_distance * 9 * dt    # I have no idea why this works.
        self.h_scrolling_offset += distance_this_frame
        self.h_remaining_distance -= distance_this_frame

        if self.h_scrolling_offset > self.h_scrolling_max:
            self.h_scrolling_offset = self.h_scrolling_max
            self.h_remaining_distance = 0
        elif self.h_scrolling_offset < self.h_scrolling_min:
            self.h_scrolling_offset = self.h_scrolling_min
            self.h_remaining_distance = 0

    def _handle_vertical_scrolling(self, dt: float):
        if not g.mouse_used:
            self.v_remaining_distance += g.mouse_wheel * 150

        if self.v_remaining_distance == 0:
            return

        self.scrolled = True
        # distance_this_frame = self.h_remaining_distance * (9/10) * dt*10
        distance_this_frame = self.v_remaining_distance * 9 * dt        # I have no idea why this works.
        self.v_scrolling_offset += distance_this_frame
        self.v_remaining_distance -= distance_this_frame

        if self.v_scrolling_offset > self.v_scrolling_max:
            self.v_scrolling_offset = self.v_scrolling_max
            self.v_remaining_distance = 0
        elif self.v_scrolling_offset < self.v_scrolling_min:
            self.v_scrolling_offset = self.v_scrolling_min
            self.v_remaining_distance = 0

    def set_scrolling_flags(self, h: bool, v: bool):
        self.enable_h_scrolling = h
        self.enable_v_scrolling = v

    def set_scrolling_proportions(self, h_min: float, h_max: float, v_min: float, v_max: float):
        self.h_scrolling_min = h_min
        self.h_scrolling_max = h_max
        self.v_scrolling_min = v_min
        self.v_scrolling_max = v_max

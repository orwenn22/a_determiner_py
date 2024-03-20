import pyray

from engine.widget import widgetmanager
from engine import globals as g


class Window:
    def __init__(self, x: int, y: int, w: int, h: int):
        from engine.windows import windowmanager

        self.title_bar_height = 15
        self.x = x
        self.y = y
        self.width = w
        self.height = h + self.title_bar_height
        self.widget_manager = widgetmanager.WidgetManager(self.x, self.y + self.title_bar_height, self.width, self.height - self.title_bar_height)
        self.manager: windowmanager.WindowManager | None = None

        # General customisation
        self.background_color = pyray.GRAY
        self.outline_color = pyray.WHITE
        self.title_bar_color = pyray.BLUE
        self.title_color = pyray.WHITE
        self.title = "Window"
        self.closable = True

        # used for dragging the window
        self.follow_mouse = False
        self.mouse_offset_x = 0
        self.mouse_offset_y = 0

    def update(self, dt: float):
        relative_mouse_x = pyray.get_mouse_x() - self.x
        relative_mouse_y = pyray.get_mouse_y() - self.y
        is_mouse_hovering = (0 <= relative_mouse_x < self.width and 0 <= relative_mouse_y < self.height)

        if self.follow_mouse:
            self.x = pyray.get_mouse_x() - self.mouse_offset_x
            self.y = pyray.get_mouse_y() - self.mouse_offset_y
            self.widget_manager.set_position(self.x, self.y+self.title_bar_height)

            if not g.is_mouse_button_down(pyray.MouseButton.MOUSE_BUTTON_LEFT):
                self.follow_mouse = False

        # This must be done before updating the widget manager, because widgets can set g.mouse_used to true
        if (not g.mouse_used) and is_mouse_hovering and g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            self._bring_on_top()

        # We update the widget manager even when the mouse is not hovering the window just in case
        self.widget_manager.update(dt)

        if (not is_mouse_hovering) or g.mouse_used:
            return
        # If we get here it means that the mouse is hovering the window

        # Clicking on title bar
        if relative_mouse_y < self.title_bar_height and g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            if relative_mouse_x >= self.width - self.title_bar_height:      # Use title bar height as close button width
                if self.closable:
                    self._close()
                # g.mouse_used = True; return
            else:       # Dragging winow
                self.mouse_offset_x = relative_mouse_x
                self.mouse_offset_y = relative_mouse_y
                self.follow_mouse = True

        g.mouse_used = True

    def draw(self):
        pyray.draw_rectangle(self.x, self.y, self.width, self.height, self.background_color)
        pyray.draw_rectangle(self.x, self.y, self.width, self.title_bar_height, self.title_bar_color)
        pyray.draw_text(self.title, self.x + 2, self.y + 2, 10, self.title_color)
        pyray.draw_rectangle(self.x+self.width-self.title_bar_height, self.y, self.title_bar_height, self.title_bar_height, pyray.RED if self.closable else pyray.GRAY)
        self.widget_manager.draw()
        pyray.draw_rectangle_lines(self.x, self.y, self.width, self.height, self.outline_color)

    def add_widget(self, widget):
        """
        Small shortcut for adding a widget in the window
        """
        self.widget_manager.add_widget(widget)

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y
        self.widget_manager.set_position(self.x, self.y + self.title_bar_height)

    def set_size(self, w: int, h: int):
        """
        Note : this set the size of the widget manager of the window.
        """
        self.width = w
        self.height = h + self.title_bar_height
        self.widget_manager.set_size(self.width, self.height - self.title_bar_height)

    def _close(self):
        if self.manager is None:
            print("No window manager, can't close window :(")
            return
        self.manager.remove_window(self)

    def _bring_on_top(self):
        if self.manager is None:
            print("No window manager, can't bring on top window :(")
            return
        self.manager.bring_on_top(self)

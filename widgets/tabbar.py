import pyray

from engine import globals as g
from engine.widget import widget
from utils import tabbarprovider


class TabBar(widget.Widget):
    # TODO : currently this is hardcoded to be at the top of the WidgetManager
    def __init__(self, provider: tabbarprovider.TabBarProvider):
        super().__init__(0, 0, 0, 22, "TL")
        self.provider = provider
        self.inner_tab_marge = 3        # 3 px on each sides

    def update(self):
        self._update_width()

        if (not self.is_hovered()) or g.mouse_used:
            return

        # If we get here, the tabbar is hovered and the mouse have not been used yet

        if g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            self._handle_click()


        g.mouse_used = True

    def draw(self):
        pyray.draw_rectangle(int(self.coordinate.x), int(self.coordinate.y), self.width, self.height, pyray.BLACK)

        if self.provider is None:
            return

        painter_x = int(self.coordinate.x)
        tab_count = self.provider.get_tab_count()
        selected_tab = self.provider.get_selected_tab()
        for i in range(tab_count):
            tab_name = self.provider.get_tab_name(i)
            tab_width = pyray.measure_text(tab_name, 20) + self.inner_tab_marge*2

            pyray.draw_rectangle(painter_x, int(self.coordinate.y), tab_width, self.height, (45, 45, 45, 255) if (i == selected_tab) else pyray.BLACK)
            pyray.draw_text(tab_name, painter_x+3, int(self.coordinate.y)+2, 20, pyray.WHITE)
            pyray.draw_line(painter_x+tab_width, int(self.coordinate.y), painter_x+tab_width, int(self.coordinate.y)+self.height, pyray.WHITE)

            painter_x += tab_width

    def _update_width(self):
        new_width = 0
        if self.manager is None:
            new_width = pyray.get_screen_width()
        else:
            new_width = self.manager.width

        if new_width != self.width:
            self.set_width(new_width)

    def _handle_click(self):
        """
        handle a click on the tabbar by the user
        """
        relative_mouse_x = int(pyray.get_mouse_x() - self.coordinate.x)
        relative_mouse_y = int(pyray.get_mouse_y() - self.coordinate.y)

        tab_count = self.provider.get_tab_count()
        top_left_x = int(self.coordinate.x)     # This is the position of the top left of the current tab
        for i in range(tab_count):
            tab_name = self.provider.get_tab_name(i)
            tab_width = pyray.measure_text(tab_name, 20) + self.inner_tab_marge*2

            if top_left_x <= relative_mouse_x < top_left_x + tab_width:
                self.provider.on_tab_click(i)
                return

            top_left_x += tab_width

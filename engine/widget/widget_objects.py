import pyray
from .. import utils
from .. import globals as g


def default_func():
    return 0


class Widget():
    def __init__(self, x: int, y: int, width: int, height: int, color, act=default_func, label: str = "", fontsize: int = 20):
        self.coordinate = pyray.Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.label = label
        self.touched: bool
        self.action = act
        self.fontsize = fontsize

    def reload_size(self, width_difference: float, height_difference: float):
        self.coordinate.x = self.coordinate.x*width_difference
        self.coordinate.y = self.coordinate.y*height_difference
        self.width = int(self.width*width_difference)
        self.height = int(self.height*height_difference)
        fontwidth = int(self.fontsize*width_difference)
        fontheight = int(self.fontsize*height_difference)
        self.fontsize = min(fontwidth, fontheight)

    def draw(self):
        pyray.draw_rectangle_pro(pyray.Rectangle(self.coordinate.x, self.coordinate.y,
                                 self.width, self.height), pyray.Vector2(0, 0), 0, self.color)
        if self.label != "":
            pyray.draw_text(self.label, int(self.coordinate.x), int(
                self.coordinate.y), self.fontsize, pyray.Color(0, 0, 0, 255))

    def checking_pressed(self):
        pos: tuple[int, int] = (pyray.get_mouse_x(), pyray.get_mouse_y())
        if utils.check_collision_mouse_rect(pos, (int(self.coordinate.x), int(self.coordinate.y), self.width, self.height)) and g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            print("1")
            self.action()

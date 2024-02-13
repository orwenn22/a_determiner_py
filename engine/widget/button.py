import pyray
from .. import utils
from .. import globals as g

from . import widget


def default_func():
    return 0


class Button(widget.Widget):
    def __init__(self, x: int, y: int, width: int, height: int, placement: str = "TL", color: pyray.Color = (100, 100, 100, 255), act=default_func, label: str = "", fontsize: int = 20, fontcolor: pyray.Color = (0, 0, 0, 255)):
        """

        :param x: placement of the widget in the window (relatively to the placement given as a string if given)
        :param y: placement of the widget in the window (relatively to the placement given as a string if given)
        :param width: Width of the widget
        :param height: Height of the widget
        :param color: Color of the background of the widget
        :param placement: relative placement in the window of the widget : TL,TC,TR,ML,MC,MR,BL,BC,BR (T=top,M=middle,B=bottom,L=left,C=center,R=right)
        :param act: callback function used as the button action
        :param label: String to be displayed on the button
        :param fontsize: integer for the fontsize 
        :param fontcolor: tuple of 4 int for the color (RGBA)

        """
        super().__init__(x, y, width, height, placement)
        self.color = color
        self.label = label
        self.touched: bool
        self.action = act
        self.fontsize = fontsize
        self.fontcolor = fontcolor

    def update(self):
        pos: tuple[int, int] = (pyray.get_mouse_x(), pyray.get_mouse_y())
        if utils.check_collision_mouse_rect(pos, (int(self.coordinate.x), int(self.coordinate.y), self.width, self.height)) and g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            self.action()

    def draw(self):
        pyray.draw_rectangle_pro(pyray.Rectangle(self.coordinate.x, self.coordinate.y, self.width, self.height),
                                 pyray.Vector2(0, 0), 0, self.color)

        if self.label != "":
            pyray.draw_text(self.label, int(self.coordinate.x+2), int(self.coordinate.y), self.fontsize, self.fontcolor)

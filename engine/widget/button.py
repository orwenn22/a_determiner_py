import pyray
from .. import utils
from .. import globals as g

from . import widget


def default_func():
    return 0


class Button(widget.Widget):
    def __init__(self, x: int, y: int, width: int, height: int, placement: str = "TL", act=default_func, label: str = ""):
        """

        :param x: placement of the widget in the window (relatively to the placement given as a string if given)
        :param y: placement of the widget in the window (relatively to the placement given as a string if given)
        :param width: Width of the widget
        :param height: Height of the widget
        :param placement: relative placement in the window of the widget : TL,TC,TR,ML,MC,MR,BL,BC,BR (T=top,M=middle,B=bottom,L=left,C=center,R=right)
        :param act: callback function used as the button action
        :param label: String to be displayed on the button

        """
        super().__init__(x, y, width, height, placement)
        self.color = pyray.Color(100, 100, 100, 255)
        self.hovering_color = self.color
        self.label = label
        self.action = act
        self.fontsize = 20
        self.fontcolor = pyray.Color(0, 0, 0, 255)

        # Internal offset of the text
        self.text_offset_x = 2
        self.text_offset_y = 0

        # If the button is hovered then its drawing position will be shifted by this amount
        self.hover_offset_x = 0
        self.hover_offset_y = 3

        # True if the button is hovered, mostly intended for subclasses
        self.hovered = False

    def update(self):
        self.hovered = False
        if g.mouse_used:
            return

        if self.is_hovered():
            self.hovered = True
            if g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
                self.action()
            g.mouse_used = True

    def draw(self):
        position_x = self.coordinate.x + self.hover_offset_x*self.hovered
        position_y = self.coordinate.y + self.hover_offset_y*self.hovered
        pyray.draw_rectangle_pro(pyray.Rectangle(position_x, position_y, self.width, self.height),
                                 pyray.Vector2(0, 0), 0, self.hovering_color if self.hovered else self.color)

        if self.label != "":
            pyray.draw_text(self.label, int(position_x+self.text_offset_x), int(position_y+self.text_offset_y),
                            self.fontsize, self.fontcolor)

    def set_color(self, color: pyray.Color, replace_hovering: bool):
        self.color = color
        if replace_hovering:
            self.hovering_color = color
        return self

    def set_hovering_color(self, color: pyray.Color):
        self.hovering_color = color
        return self

    def set_font_color(self, color: pyray.Color):
        self.fontcolor = color
        return self

    def set_font_size(self, font_size: int):
        self.fontsize = font_size
        return self

    def set_text_offset(self, x: int, y: int):
        self.text_offset_x = x
        self.text_offset_y = y
        return self

    def center_text(self):
        self.text_offset_x = (self.width - pyray.measure_text(self.label, self.fontsize))//2
        self.text_offset_y = (self.height - self.fontsize)//2
        return self

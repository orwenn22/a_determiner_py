import pyray

from . import button


def default_func():
    return 0


class TexturedButton(button.Button):
    def __init__(self, x: int, y: int, width: int, height: int, sprite: pyray.Texture, placement: str = "TL", act=default_func, label: str = ""):
        """

        :param x: placement of the widget in the window (relatively to the placement given as a string if given)
        :param y: placement of the widget in the window (relatively to the placement given as a string if given)
        :param width: Width of the widget
        :param height: Height of the widget
        :param sprite: sprite used for the widget
        :param placement: relative placement in the window of the widget : TL,TC,TR,ML,MC,MR,BL,BC,BR (T=top,M=middle,B=bottom,L=left,C=center,R=right)
        :param act: callback function used as the button action
        :param label: String to be displayed on the button

        """
        super().__init__(x, y, width, height, placement, act, label)
        self.sprite = sprite
        self.color = pyray.WHITE
        self.hovering_color = self.color

    def draw(self):
        position_x = self.coordinate.x + self.hover_offset_x * self.hovered
        position_y = self.coordinate.y + self.hover_offset_y * self.hovered

        pyray.draw_texture_pro(self.sprite,
                               pyray.Rectangle(0, 0, self.sprite.width, self.sprite.height),
                               pyray.Rectangle(position_x, position_y, self.width, self.height),
                               pyray.Vector2(0, 0), 0,
                               self.hovering_color if self.hovered else self.color)
        if self.label != "":
            pyray.draw_text(self.label, int(position_x+self.text_offset_x), int(position_y+self.text_offset_y), self.fontsize, self.fontcolor)

import pyray
from .. import utils
from .. import globals as g


def default_func():
    return 0


class Widget():
    def __init__(self, x: int, y: int, width: int, height: int, color, placement: str = "TL", act=default_func, label: str = "", fontsize: int = 20, fontcolor: tuple[int, int, int, int] = (0, 0, 0, 255)):
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
        self.origin = pyray.Vector2(x, y)

        match(placement[0]):
            case "M":
                y = int(pyray.get_screen_height()/2) + y-int(height/2)
            case "B":
                y = pyray.get_screen_height() - height
        match(placement[1]):
            case "C":
                x = int(pyray.get_screen_width()/2) + x - int(height/2)
            case "R":
                x = pyray.get_screen_width() - width

        self.coordinate = pyray.Vector2(x, y)
        self.width = width
        self.height = height
        self.color = color
        self.label = label
        self.touched: bool
        self.action = act
        self.fontsize = fontsize
        self.fontcolor = fontcolor
        self.placement = placement

    def reload_placement(self):
        """
        function used only in case of window resizing to keep widgets to the right spot
        """
        match(self.placement[0]):
            case "M":
                self.coordinate.y = int(pyray.get_screen_height()/2) + self.origin.y - int(self.height/2)
            case "B":
                self.coordinate.y = pyray.get_screen_height() - self.height
        match(self.placement[1]):
            case "C":
                self.coordinate.x = int(pyray.get_screen_width()/2) + self.origin.x - int(self.height/2)
            case "R":
                self.coordinate.x = pyray.get_screen_width() - self.width

    def draw(self):
        pyray.draw_rectangle_pro(pyray.Rectangle(self.coordinate.x, self.coordinate.y,
                                 self.width, self.height), pyray.Vector2(0, 0), 0, self.color)
        if self.label != "":
            pyray.draw_text(self.label, int(self.coordinate.x), int(
                self.coordinate.y), self.fontsize, self.fontcolor)

    def checking_pressed(self):
        pos: tuple[int, int] = (pyray.get_mouse_x(), pyray.get_mouse_y())
        if utils.check_collision_mouse_rect(pos, (int(self.coordinate.x), int(self.coordinate.y), self.width, self.height)) and g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            self.action()

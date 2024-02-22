import pyray


class Widget(object):
    def __init__(self, x: int, y: int, width: int, height: int, placement: str = "TL"):
        """
        Base constructor of a widget
        :param x: placement of the widget in the window (relatively to the placement given as a string if given)
        :param y: placement of the widget in the window (relatively to the placement given as a string if given)
        :param width: Width of the widget
        :param height: Height of the widget
        :param placement: relative placement in the window of the widget : TL,TC,TR,ML,MC,MR,BL,BC,BR (T=top,M=middle,B=bottom,L=left,C=center,R=right)
        """
        self.origin = pyray.Vector2(x, y)       # relative position from alignment/placement
        self.coordinate = pyray.Vector2(x, y)   # absolute position on window
        self.width = width
        self.height = height
        self.placement = placement
        self.reload_placement()

    def reload_placement(self):
        """
        function used only in case of window resizing to keep widgets to the right spot
        """
        match(self.placement[0]):
            case "M":
                self.coordinate.y = int(pyray.get_screen_height()/2) + self.origin.y - int(self.height/2)
            case "B":
                self.coordinate.y = pyray.get_screen_height() - self.height - self.origin.y
            case _:
                self.coordinate.y = self.origin.y
        match(self.placement[1]):
            case "C":
                self.coordinate.x = int(pyray.get_screen_width()/2) + self.origin.x - int(self.width/2)
            case "R":
                self.coordinate.x = pyray.get_screen_width() - self.width - self.origin.x
            case _:
                self.coordinate.x = self.origin.x

    def update(self):
        pass

    def draw(self):
        pyray.draw_rectangle_pro(pyray.Rectangle(self.coordinate.x, self.coordinate.y, self.width, self.height),
                                 pyray.Vector2(0, 0), 0,
                                 pyray.Color(255, 0, 0, 255))

    def set_x(self, x: int):
        self.origin.x = x
        self.reload_placement()
        return self

    def set_y(self, y: int):
        self.origin.y = y
        self.reload_placement()
        return self

    def set_width(self, width: int):
        self.width = width
        self.reload_placement()
        return self

    def set_height(self, height: int):
        self.height = height
        self.reload_placement()
        return self

    def set_position(self, x: int, y: int):
        self.origin.x = x
        self.origin.y = y
        self.reload_placement()
        return self

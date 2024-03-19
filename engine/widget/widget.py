import pyray
from .. import utils


class Widget(object):
    def __init__(self, x: int, y: int, width: int, height: int, placement: str = "TL"):
        from . import widgetmanager as widgetmanager
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
        self.manager: widgetmanager.WidgetManager = None
        self.scrollable = True
        self.reload_placement()

    def reload_placement(self):
        """
        function used only in case of window resizing to keep widgets to the right spot
        """
        if self.manager is None:
            container_x = 0
            container_y = 0
            container_w = pyray.get_screen_width()
            container_h = pyray.get_screen_height()
        else:
            container_x = self.manager.x
            container_y = self.manager.y
            container_w = self.manager.width
            container_h = self.manager.height


        match(self.placement[0]):
            case "M":
                self.coordinate.y = container_y + container_h//2 + (self.origin.y-self.height//2)
            case "B":
                self.coordinate.y = container_y + container_h - self.height - self.origin.y
            case _:
                self.coordinate.y = container_y + self.origin.y
        match(self.placement[1]):
            case "C":
                self.coordinate.x = container_x + container_w//2 + (self.origin.x-self.width//2)
            case "R":
                self.coordinate.x = container_x + container_w - self.width - self.origin.x
            case _:
                self.coordinate.x = container_x + self.origin.x

        if self.manager is not None and self.scrollable:
            self.coordinate.x += int(self.manager.h_scrolling_offset)
            self.coordinate.y += int(self.manager.v_scrolling_offset)

    def update(self):
        pass

    def draw(self):
        pyray.draw_rectangle_pro(pyray.Rectangle(self.coordinate.x, self.coordinate.y, self.width, self.height),
                                 pyray.Vector2(0, 0), 0,
                                 pyray.Color(255, 0, 0, 255))

    def is_hovered(self) -> bool:
        return utils.check_collision_point_rect((pyray.get_mouse_x(), pyray.get_mouse_y()),
                                                (int(self.coordinate.x), int(self.coordinate.y), self.width, self.height))

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

    def set_scrollable(self, scrollable: bool):
        self.scrollable = scrollable
        return self

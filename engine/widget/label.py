import pyray

from . import widget


class Label(widget.Widget):
    def __init__(self, x: int, y: int, placement: str, text: str, font_size: int, color: pyray.Color = (255, 255, 255, 255)):
        super().__init__(x, y, 1, font_size, placement)
        self.font_size = font_size
        self.color = color
        self.text = text
        self.font: pyray.Font | None = None
        self.font_spacing = 2.0
        self._reload_width()
        self.reload_placement()

    def draw(self):
        # pyray.draw_rectangle(int(self.coordinate.x), int(self.coordinate.y), self.width, self.height, pyray.RED)
        if self.font is not None:
            pyray.draw_text_ex(self.font, self.text,
                               pyray.Vector2(self.coordinate.x, self.coordinate.y),
                               self.font_size, self.font_spacing, self.color)
        else:
            pyray.draw_text(self.text, int(self.coordinate.x), int(self.coordinate.y), int(self.font_size), self.color)

    def set_color(self, color: pyray.Color):
        self.color = color
        return self

    def set_font_size(self, font_size: int):
        self.font_size = font_size
        self._reload_width()
        self.reload_placement()
        return self

    def set_text(self, text: str):
        self.text = text
        self._reload_width()
        self.reload_placement()
        return self

    def set_font(self, font: pyray.Font, spacing: float = 2):
        self.font = font
        self.font_spacing = spacing
        self._reload_width()
        self.reload_placement()
        return self

    def _reload_width(self):
        if self.font is not None:
            text_size = self.width = pyray.measure_text_ex(self.font, self.text, self.font_size, self.font_spacing)
            self.width = text_size.x
            # TODO : y ?
        else:
            self.width = pyray.measure_text(self.text, self.font_size)

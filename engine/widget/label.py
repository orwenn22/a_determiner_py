import pyray

from . import widget


class Label(widget.Widget):
    def __init__(self, x: int, y: int, placement: str, text: str, font_size: int, color: pyray.Color = (255, 255, 255, 255)):
        super().__init__(x, y, 1, font_size, placement)
        self.font_size = font_size
        self.color = color
        self.text = text
        self.width = pyray.measure_text(text, font_size)        # TODO : if we support custom fonts one day we need to replace this by measure_text_ex
        self.reload_placement()

    def draw(self):
        # pyray.draw_rectangle(int(self.absolute_position.x), int(self.absolute_position.y), self.width, self.height, pyray.RED)
        # TODO : if we support custom fonts one day we need to replace this by draw_text_ex
        pyray.draw_text(self.text, int(self.absolute_position.x), int(self.absolute_position.y), int(self.font_size), self.color)

    def set_color(self, color: pyray.Color):
        self.color = color
        return self

    def set_font_size(self, font_size: int):
        self.font_size = font_size
        return self

    def set_text(self, text: str):
        self.text = text
        self.width = pyray.measure_text(text, self.font_size)
        self.reload_placement()
        return self

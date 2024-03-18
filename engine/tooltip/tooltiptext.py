import pyray
from . import tooltipelements

    
class TooltipText(tooltipelements.TooltipElement):
    def __init__(self, text : str, fontsize : int, color: pyray.Color):
        self.text = text
        self.fontsize = fontsize
        self.color = color

        spacing = fontsize/10
        text_size : pyray.Vector2 = pyray.measure_text_ex(pyray.get_font_default(), text, fontsize, spacing)
        super().__init__(int(text_size.x), int(text_size.y))

    def draw(self, x: int, y: int):
        spacing = self.fontsize/10
        pyray.draw_text_ex(pyray.get_font_default(), self.text, pyray.Vector2(x, y),self.fontsize,spacing, self.color)
        pyray.draw_text(self.text, x, y, self.fontsize, self.color)


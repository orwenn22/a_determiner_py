import pyray
from . import tooltipelements

    
class TooltipText(tooltipelements.TooltipElement):
    def __init__(self, text : str, fontsize : int, color: pyray.Color):
        self.m_text = text
        self.m_fontsize = fontsize
        self.m_color = color

        spacing = fontsize/10
        text_size : pyray.Vector2 = pyray.measure_text_ex(pyray.get_font_default(), text, fontsize, spacing)
        super().__init__(int(text_size.x), int(text_size.y))

    def draw(self, x: int, y: int):
        spacing = self.m_fontsize/10
        pyray.draw_text_ex(pyray.get_font_default(), self.m_text, pyray.Vector2(x, y),self.m_fontsize,spacing, self.m_color)
        pyray.draw_text(self.m_text, x, y, self.m_fontsize, self.m_color)


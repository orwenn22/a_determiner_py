import pyray
from .. import globals as g
from . import tooltipelements

class Tooltip():
    def __init__(self):
        self.elements: list[tooltipelements.TooltipElement] = []
    
    def add_elements(self,element :tooltipelements.TooltipElement):
        self.elements.append(element)

    def clear_elements(self):
        self.elements.clear()

    def draw(self, x:int, y:int):
        width = 0
        height = 0
        for e in self.elements:
            height = e.m_height + 2
            w = e.m_width
            if w > width:
                width = w

        if (width == 0 or height == 0):
            return
        
        width += 4
        height +=2

        if x+width >= pyray.get_render_width():
            x -= width + 3
        if y+height >= pyray.get_render_height():
            y -= height + 3

        pyray.draw_rectangle(int(x), int(y), int(width), int(height), pyray.BLACK)
        pyray.draw_rectangle_lines(int(x), int(y), int(width), int(height), pyray.WHITE)

        painter_y = 2
        for e in self.elements:
            e.draw(x+2, y + painter_y)
            painter_y += e.m_height + 2

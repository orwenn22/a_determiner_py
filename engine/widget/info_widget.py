import pyray
from . import widget
from .. import globals as g
from ..tooltip import tooltiptext, tooltip

class InfoWidget(widget.Widget):
    def __init__(self, x: int, y: int, width: int, height: int, widget_image: pyray.Texture, info_text: str, tooltip: tooltip.Tooltip, placement: str = "TL", fontsize:int = 20):
        super().__init__(x,y,width,height,placement)
        self.image = widget_image
        self.info = info_text
        self.fontsize = fontsize
        self.text_size = pyray.measure_text_ex(pyray.get_font_default(), self.info, self.fontsize + 10, 2)
        # Using top left for the widget as we use directly where the mouse is
        self.tooltip = tooltip
        

    def update(self):
        if self.is_hovered():
            self.tooltip.add_elements(tooltiptext.TooltipText(self.info, self.fontsize, pyray.WHITE))
             
    def draw(self):
       pyray.draw_texture_pro(self.image, pyray.Rectangle(0, 0, self.image.width, self.image.height), pyray.Rectangle(self.coordinate.x, self.coordinate.y, self.width, self.height),pyray.Vector2(0, 0),0,pyray.WHITE) 


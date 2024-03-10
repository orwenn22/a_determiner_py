import pyray
from . import widget, tiledwidget
from .. import globals as g
import globalresources as res

class InfoWidget(widget.Widget):
    def __init__(self, x: int, y: int, width: int, height: int, widget_image: pyray.Texture, info_text: str, placement: str = "TL", fontsize:int = 20):
        super().__init__(x,y,width,height,placement)
        self.image = widget_image
        self.info = info_text
        self.hovered = False 
        self.fontsize = fontsize
        self.text_size = pyray.measure_text_ex(pyray.get_font_default(),self.info,self.fontsize + 10,2)
        # Using top left for the widget as we use directly where the mouse is
        self.infowidget = tiledwidget.TiledWidget(0, 0, self.text_size.x, self.text_size.y, "TL", res.tiled_button_sprite, 8, 2, self.info)
        
    def update(self):
        if self.is_hovered() and not self.hovered:
            self.hovered = True
            self.manager.add_widget(self.infowidget) 
            self.infowidget.set_position(int(pyray.get_mouse_x()),int(pyray.get_mouse_y() + self.text_size.y)) 
        elif self.is_hovered() and self.hovered:
            self.infowidget.set_position(int(pyray.get_mouse_x()),int(pyray.get_mouse_y() + self.text_size.y))
        elif not self.is_hovered() and self.hovered:
            self.hovered = False
            self.manager.remove_widget(self.infowidget)

    def draw(self):
       pyray.draw_texture_pro(self.image, pyray.Rectangle(0, 0, self.image.width, self.image.height), pyray.Rectangle(self.coordinate.x, self.coordinate.y, self.width, self.height),pyray.Vector2(0, 0),0,pyray.WHITE) 


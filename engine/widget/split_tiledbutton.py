from . import tiledbutton
from . import button
import pyray
import globalresources as res


class SplitTiledButton(tiledbutton.TiledButton):
    def __init__(self, x: int, y: int, width: int, height: int, placement: str, tile_set: pyray.Texture, tile_size: int, leftimage: pyray.Texture = res.default_void_sprite, scale: int = 1, label: str = "", act=button.default_func):
        super().__init__(x, y, width, height, placement, tile_set, tile_size, scale, act=act)
        self.leftimage = leftimage
        self.label = label
        self.center_text()

    def update(self):
        super().update()

    def draw(self):
        super()._draw_tiles()

        pos_x = self.coordinate.x + self.hover_offset_x * self.hovered
        pos_y = self.coordinate.y + self.hover_offset_y * self.hovered
        pyray.draw_texture_pro(self.leftimage, pyray.Rectangle(0, 0, self.leftimage.width, self.leftimage.height),
                               pyray.Rectangle(pos_x + 5, pos_y + 5, self.width/2-10, self.height-10),
                               pyray.Vector2(0, 0), 0,
                               pyray.Color(255, 255, 255, 255))

        pyray.draw_text(self.label,
                        int(pos_x+self.width//2 + self.text_offset_x),
                        int(pos_y + self.text_offset_y),
                        self.fontsize, pyray.Color(128, 128, 128, 255))

    def center_text(self):
        self.text_offset_x = (self.width/2 - pyray.measure_text(self.label, self.fontsize)) // 2
        self.text_offset_y = (self.height - self.fontsize) // 2
        return self

from . import widget
import pyray


class TiledWidget(widget.Widget):
    def __init__(self, x: int, y: int, width: int, height: int, placement: str, tile_set: pyray.Texture, tile_size: int, scale: int = 1, label: str = ""):
        super().__init__(x, y, width, height, placement)
        self.tile_set = tile_set
        self.tile_size = tile_size
        self.scale = scale
        self.color = pyray.WHITE
        self.label = label
        self.fontsize = 20
        self.fontcolor = pyray.WHITE
        self.offset_x = 10
        self.offset_y = 5

    def update(self):
        super().update()

    def draw(self):
        self._draw_tiles()

        if self.label != "":
            pyray.draw_text(self.label, int(self.coordinate.x + self.offset_x), int(self.coordinate.y + self.offset_y), self.fontsize, self.fontcolor)

    def _draw_tiles(self):

        scaled_size = self.tile_size * self.scale
        # Top left
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(0, 0, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x, self.coordinate.y, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Top right
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(self.tile_size * 2, 0, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x + self.width - scaled_size, self.coordinate.y, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Bottom left
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(0, self.tile_size * 2, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x, self.coordinate.y + self.height - scaled_size, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Bottom right
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(self.tile_size * 2, self.tile_size * 2, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x + self.width - scaled_size, self.coordinate.y + self.height - scaled_size, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Top
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(self.tile_size, 0, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x + scaled_size, self.coordinate.y, self.width - (scaled_size * 2), scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Left
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(0, self.tile_size, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x, self.coordinate.y + scaled_size, scaled_size, self.height - (scaled_size * 2)),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Right
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(self.tile_size * 2, self.tile_size, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x + self.width - scaled_size, self.coordinate.y + scaled_size, scaled_size, self.height - (scaled_size * 2)),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Bottom
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(self.tile_size, self.tile_size * 2, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x + scaled_size, self.coordinate.y + self.height - scaled_size, self.width - (scaled_size * 2), scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

        # Center
        pyray.draw_texture_pro(self.tile_set,
                               pyray.Rectangle(self.tile_size, self.tile_size, self.tile_size, self.tile_size),
                               pyray.Rectangle(self.coordinate.x + scaled_size, self.coordinate.y + scaled_size, self.width - (scaled_size * 2), self.height - (scaled_size * 2)),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

    def set_offset_text(self, offset_x:int, offset_y:int):
        self.offset_x = offset_x
        self.offset_y = offset_y

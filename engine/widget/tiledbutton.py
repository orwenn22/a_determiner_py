from . import button
import pyray


class TiledButton(button.Button):
    def __init__(self, x: int, y: int, width: int, height: int, placement: str, tile_set: pyray.Texture, tile_size: int, scale: int = 1, label: str = "", act=button.default_func):
        super().__init__(x, y, width, height, placement, act, label)
        self.tile_set = tile_set
        self.hover_tile_set = tile_set
        self.tile_size = tile_size
        self.scale = scale
        self.color = pyray.WHITE
        self.hovering_color = self.color

    def update(self):
        super().update()

    def draw(self):
        position_x = self.coordinate.x + self.hover_offset_x * self.hovered
        position_y = self.coordinate.y + self.hover_offset_y * self.hovered
        current_texture = self.hover_tile_set if self.hovered else self.tile_set
        current_color = self.hovering_color if self.hovered else self.color

        scaled_size = self.tile_size * self.scale
        # Top left
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(0, 0, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x, position_y, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Top right
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(self.tile_size*2, 0, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x+self.width-scaled_size, position_y, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Bottom left
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(0, self.tile_size*2, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x, position_y+self.height-scaled_size, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Bottom right
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(self.tile_size*2, self.tile_size*2, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x+self.width-scaled_size, position_y+self.height-scaled_size, scaled_size, scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Top
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(self.tile_size, 0, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x+scaled_size, position_y, self.width-(scaled_size*2), scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Left
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(0, self.tile_size, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x, position_y+scaled_size, scaled_size, self.height-(scaled_size*2)),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Right
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(self.tile_size*2, self.tile_size, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x+self.width-scaled_size, position_y+scaled_size, scaled_size, self.height-(scaled_size*2)),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Bottom
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(self.tile_size, self.tile_size*2, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x+scaled_size, position_y+self.height-scaled_size, self.width-(scaled_size*2), scaled_size),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Center
        pyray.draw_texture_pro(current_texture,
                               pyray.Rectangle(self.tile_size, self.tile_size, self.tile_size, self.tile_size),
                               pyray.Rectangle(position_x+scaled_size, position_y+scaled_size, self.width-(scaled_size*2), self.height-(scaled_size*2)),
                               pyray.Vector2(0, 0), 0.0,
                               current_color)

        # Wow, this is long, pls send help.
        # Now we draw the text
        super()._draw_text()

    def set_tile_set(self, tile_set: pyray.Texture, replace_hovering=False):
        if tile_set is not None:
            self.tile_set = tile_set
            if replace_hovering:
                self.hover_tile_set = tile_set
        return self

    def set_hovering_tile_set(self, tile_set: pyray.Texture):
        if tile_set is not None:
            self.hover_tile_set = tile_set
        return self

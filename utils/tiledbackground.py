import pyray


class TiledBackground:
    def __init__(self, tile_texture: pyray.Texture, color: tuple[int, int, int, int] = pyray.WHITE):
        self.tile_texture = tile_texture
        self.color = color
        self.scale = 1
        self.scrolling = pyray.Vector2(0, 0)

    def update(self, dt: float):
        self.scrolling.x += 12 * dt
        self.scrolling.y += 12 * dt

    def draw(self):
        pyray.draw_texture_pro(self.tile_texture,
                               pyray.Rectangle(self.scrolling.x, self.scrolling.y, pyray.get_screen_width()/self.scale, pyray.get_screen_height()/self.scale),
                               pyray.Rectangle(0, 0, pyray.get_screen_width(), pyray.get_screen_height()),
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

    def set_scrolling(self, scroll_x: float, scroll_y: float):
        self.scrolling.x = scroll_x
        self.scrolling.y = scroll_y

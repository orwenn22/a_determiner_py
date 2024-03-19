import pyray


class TiledBackground:
    def __init__(self, tile_texture: pyray.Texture, rec: tuple[int, int, int, int] = (0, 0, 0, 0), color: tuple[int, int, int, int] = pyray.WHITE):
        self.tile_texture = tile_texture
        self.color = color
        self.scale = 1
        self.scrolling = pyray.Vector2(0, 0)
        self.rec = rec
        self.fullscreen = (rec == (0, 0, 0, 0))

    def update(self, dt: float):
        self.scrolling.x += 12 * dt
        self.scrolling.y += 12 * dt

    def draw(self):
        rec = pyray.Rectangle(0, 0, pyray.get_screen_width(), pyray.get_screen_height()) if self.fullscreen \
            else pyray.Rectangle(self.rec[0], self.rec[1], self.rec[2], self.rec[2])

        pyray.draw_texture_pro(self.tile_texture,
                               pyray.Rectangle(self.scrolling.x, self.scrolling.y, pyray.get_screen_width()/self.scale, pyray.get_screen_height()/self.scale),
                               rec,
                               pyray.Vector2(0, 0), 0.0,
                               self.color)

    def set_scrolling(self, scroll_x: float, scroll_y: float):
        self.scrolling.x = scroll_x
        self.scrolling.y = scroll_y

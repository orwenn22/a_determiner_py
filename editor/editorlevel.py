import pyray

from utils.valref import ValRef


class EditorLevel:
    def __init__(self):
        self.name = "no_name"
        self.tileset: pyray.Texture | None = None

        # Size in pixel of a single tile
        self.tile_width = ValRef(16)
        self.tile_height = ValRef(16)

        # Size of the level in tiles
        self.level_horizontal_tiles = ValRef(16)
        self.level_vertical_tiles = ValRef(16)

        # Tile data of the level
        self.tilemap = [0] * self.level_horizontal_tiles.get() * self.level_vertical_tiles.get()

        self.level_width_meter = ValRef(16)
        self.level_height_meter = ValRef(16)

    def set_tile(self, x: int, y: int, v: int):
        if not (0 <= x < self.level_horizontal_tiles.get() and 0 <= y < self.level_vertical_tiles.get()):
            return
        self.tilemap[x + y * self.level_horizontal_tiles.get()] = v

    def set_tilemap_size(self, w: int, h: int):
        if w <= 0 or h <= 0:
            return

        new_tilemap = [0] * w * h
        for y in range(0, min(h, self.level_vertical_tiles.get())):
            for x in range(0, min(w, self.level_horizontal_tiles.get())):
                new_tilemap[x+y*w] = self.tilemap[x+y*self.level_horizontal_tiles.get()]

        self.level_horizontal_tiles.set(w)
        self.level_vertical_tiles.set(h)
        self.tilemap = new_tilemap

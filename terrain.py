import pyray

from engine import graphics as gr
import math


class Terrain(object):
    def __init__(self, sprite_path: str, size: pyray.Vector2):
        """
        Create a new terrain
        :param sprite_path: path to the bitmap to use
        :param size: size of the map in meter
        """
        self.image = pyray.load_image(sprite_path)                  # on cpu
        self.texture = pyray.load_texture_from_image(self.image)    # on gpu
        self.size = size                                            # Size of terrain in meter

        self.collision_mask = []
        print("terrain : calculating terrain mesh...")
        image_colors = pyray.load_image_colors(self.image)
        for y in range(self.image.height):
            for x in range(self.image.width):
                alpha = image_colors[x+y*self.image.width].a
                self.collision_mask.append(alpha != 0)
        pyray.unload_image_colors(image_colors)
        print("terrain : done ! :D")

    def unload(self):
        pyray.unload_texture(self.texture)
        pyray.unload_image(self.image)
        print("terrain : unloaded")

    def check_collision(self, position: pyray.Vector2, outside_solid: bool = False):
        """

        position: position in meter
        """
        pixel_x = int(position.x / self.size.x * self.image.width)
        pixel_y = int(position.y / self.size.y * self.image.height)

        if pixel_x < 0 or pixel_x >= self.image.width or pixel_y < 0 or pixel_y >= self.image.height:
            return outside_solid
        return self.collision_mask[pixel_x + pixel_y * self.image.width]

    def check_collision_rec(self, rectangle: tuple[float, float, float, float], outside_solid: bool = False):
        """

        rectangle: hitbox in meter we want to check collision for
        """
        # Top left
        pixel_x = int(rectangle[0] / self.size.x * self.image.width)
        pixel_y = int(rectangle[1] / self.size.y * self.image.height)
        # Bottom right
        pixel_x2 = int((rectangle[0] + rectangle[2]) / self.size.x * self.image.width)
        pixel_y2 = int((rectangle[1] + rectangle[3]) / self.size.y * self.image.height)
        # print(pixel_x, pixel_y, pixel_x2, pixel_y2)

        if outside_solid:
            if pixel_x < 0 or pixel_x2 >= self.image.width or pixel_y < 0 or pixel_y2 >= self.image.height: return True
        else:
            # We want to only check pixels that are in bounce
            if pixel_x < 0: pixel_x = 0
            if pixel_x2 >= self.image.width: pixel_x2 = self.image.width - 1
            if pixel_y < 0: pixel_y = 0
            if pixel_y2 >= self.image.height: pixel_y2 = self.image.height - 1

        # Left & right
        if not (pixel_x >= self.image.width or pixel_x2 < 0):
            for y in range(pixel_y, pixel_y2+1):
                if self.collision_mask[pixel_x + y * self.image.width] or self.collision_mask[pixel_x2 + y * self.image.width]:
                    return True

        # Top & bottom
        if not (pixel_y >= self.image.height or pixel_y2 < 0):
            for x in range(pixel_x, pixel_x2+1):
                if self.collision_mask[x + pixel_y * self.image.width] or self.collision_mask[x + pixel_y2 * self.image.width]:
                    return True

        # Center    (only check 1/9 of the pixels to save time)
        for y in range(pixel_y+1, pixel_y2, 3):
            for x in range(pixel_x+1, pixel_x2, 3):
                if self.collision_mask[x + y * self.image.width]:
                    return True

        return False

    def destroy_rectangle(self, rectangle: tuple[float, float, float, float]):
        pixel_x = int(rectangle[0] / self.size.x * self.image.width)
        pixel_y = int(rectangle[1] / self.size.y * self.image.height)
        pixel_x2 = int((rectangle[0] + rectangle[2]) / self.size.x * self.image.width)
        pixel_y2 = int((rectangle[1] + rectangle[3]) / self.size.y * self.image.height)

        if pixel_x < 0: pixel_x = 0
        if pixel_x2 >= self.image.width: pixel_x2 = self.image.width - 1
        if pixel_y < 0: pixel_y = 0
        if pixel_y2 >= self.image.height: pixel_y2 = self.image.height - 1

        for y in range(pixel_y, pixel_y2 + 1):
            for x in range(pixel_x, pixel_x2 + 1):
                self.collision_mask[x + y * self.image.width] = False
                pyray.image_draw_pixel(self.image, x, y, pyray.Color(0, 0, 0, 0))
        self.update_sprite()

    def destroy_circle(self, center: pyray.Vector2, radius: float):
        # TODO : currently this doesn't take the height into account
        radius_pixel = int(radius / self.size.x * self.image.width)
        self.destroy_circle_pixel(center, radius_pixel)

    def destroy_circle_pixel(self, center: pyray.Vector2, radius_pixel: int):
        pixel_x = int(center.x / self.size.x * self.image.width)
        pixel_y = int(center.y / self.size.y * self.image.height)

        step_count = int(radius_pixel * 3.14)

        previous_xpos = -99999
        for i in range(0, step_count):
            x_pos = pixel_x + int(math.cos(i * math.pi / step_count) * radius_pixel)  # x position
            if x_pos == previous_xpos: continue
            previous_xpos = x_pos

            if x_pos < 0:
                continue
            elif x_pos >= self.image.width:
                continue

            y_dist = int(math.sin(i * math.pi / step_count) * radius_pixel)  # y distance from the x axes

            for y in range(pixel_y - y_dist, pixel_y + y_dist + 1):
                if y < 0:
                    continue
                elif y >= self.image.height:
                    continue
                self.collision_mask[x_pos + y * self.image.width] = False
                pyray.image_draw_pixel(self.image, x_pos, y, pyray.Color(0, 0, 0, 0))
        self.update_sprite()

    def pixel_width(self) -> float:
        return self.size.x / self.image.width

    def pixel_height(self) -> float:
        return self.size.y / self.image.height

    def update(self):
        pass

    def draw(self):
        gr.draw_sprite_scale(self.texture, (0, 0, self.size.x, self.size.y))
        gr.draw_rectangle(0, 0, self.size.x, self.size.y, pyray.Color(255, 0, 0, 255), False)

    def update_sprite(self):
        pyray.unload_texture(self.texture)
        self.texture = pyray.load_texture_from_image(self.image)

import pygame

from engine import graphics as gr, metrics as m, globals as g
import math


class Terrain(object):
    def __init__(self, bitmap: pygame.Surface, size: pygame.Vector2):
        self.bitmap = bitmap.copy()
        self.cached_texture: pygame.Surface = None
        # self.collision_mask = pygame.Surface((self.bitmap.get_width(), self.bitmap.get_height()))
        self.collision_mask = []
        for y in range(self.bitmap.get_height()):
            for x in range(self.bitmap.get_width()):
                self.collision_mask.append(self.bitmap.get_at((x, y)) != (0, 0, 0, 0))
        self.size = size.copy()
        self.update_cache()

    def check_collision(self, position: pygame.Vector2):
        """

        position: position in meter
        """
        pixel_x = int(position.x / self.size.x * self.bitmap.get_width())
        pixel_y = int(position.y / self.size.y * self.bitmap.get_height())

        if pixel_x < 0 or pixel_x >= self.bitmap.get_width() or pixel_y < 0 or pixel_y >= self.bitmap.get_height():
            return False
        return self.collision_mask[pixel_x + pixel_y*self.bitmap.get_width()]

    def check_collision_rec(self, rectangle: tuple[float, float, float, float]):
        """

        rectangle: hitbox in meter we want to check collision for
        """
        pixel_x = int(rectangle[0] / self.size.x * self.bitmap.get_width())
        pixel_y = int(rectangle[1] / self.size.y * self.bitmap.get_height())
        pixel_x2 = int((rectangle[0]+rectangle[2]) / self.size.x * self.bitmap.get_width())
        pixel_y2 = int((rectangle[1]+rectangle[3]) / self.size.y * self.bitmap.get_height())

        # print(pixel_x, pixel_y, pixel_x2, pixel_y2)

        if pixel_x < 0: pixel_x = 0
        if pixel_x2 >= self.bitmap.get_width(): pixel_x2 = self.bitmap.get_width()-1
        if pixel_y < 0: pixel_y = 0
        if pixel_y2 >= self.bitmap.get_height(): pixel_y2 = self.bitmap.get_height()-1

        for y in range(pixel_y, pixel_y2+1):
            for x in range(pixel_x, pixel_x2+1):
                if self.collision_mask[x + y*self.bitmap.get_width()]:
                    return True
        return False

    def destroy_rectangle(self, rectangle: tuple[float, float, float, float]):
        pixel_x = int(rectangle[0] / self.size.x * self.bitmap.get_width())
        pixel_y = int(rectangle[1] / self.size.y * self.bitmap.get_height())
        pixel_x2 = int((rectangle[0] + rectangle[2]) / self.size.x * self.bitmap.get_width())
        pixel_y2 = int((rectangle[1] + rectangle[3]) / self.size.y * self.bitmap.get_height())

        if pixel_x < 0: pixel_x = 0
        if pixel_x2 >= self.bitmap.get_width(): pixel_x2 = self.bitmap.get_width()-1
        if pixel_y < 0: pixel_y = 0
        if pixel_y2 >= self.bitmap.get_height(): pixel_y2 = self.bitmap.get_height()-1

        for y in range(pixel_y, pixel_y2+1):
            for x in range(pixel_x, pixel_x2+1):
                self.collision_mask[x + y*self.bitmap.get_width()] = False
                self.bitmap.set_at((x, y), (0, 0, 0, 0))

    def destroy_circle(self, center: pygame.Vector2, radius: float):
        # TODO : currently this doesn't take the height into account
        radius_pixel = int(radius / self.size.x * self.bitmap.get_width())

        pixel_x = int(center.x / self.size.x * self.bitmap.get_width())
        pixel_y = int(center.y / self.size.y * self.bitmap.get_height())

        step_count = int(radius_pixel*3.0)

        for i in range(0, step_count):
            x_pos = pixel_x + int(math.cos(i * math.pi / step_count) * radius_pixel)   # x position

            if x_pos < 0:continue
            elif x_pos >= self.bitmap.get_width():continue

            y_dist = int(math.sin(i * math.pi / step_count) * radius_pixel)    # y distance from the x axes

            for y in range(pixel_y-y_dist, pixel_y+y_dist+1):
                if y < 0: continue
                elif y >= self.bitmap.get_height(): continue
                self.collision_mask[x_pos + y * self.bitmap.get_width()] = False
                self.bitmap.set_at((x_pos, y), (0, 0, 0, 0))

        self.update_cache()

    def destroy_circle_pixel(self, center: pygame.Vector2, radius_pixel: int):
        pixel_x = int(center.x / self.size.x * self.bitmap.get_width())
        pixel_y = int(center.y / self.size.y * self.bitmap.get_height())

        step_count = int(radius_pixel*3.0)

        for i in range(0, step_count):
            x_pos = pixel_x + int(math.cos(i * math.pi / step_count) * radius_pixel)   # x position

            if x_pos < 0:continue
            elif x_pos >= self.bitmap.get_width():continue

            y_dist = int(math.sin(i * math.pi / step_count) * radius_pixel)    # y distance from the x axes

            for y in range(pixel_y-y_dist, pixel_y+y_dist+1):
                if y < 0: continue
                elif y >= self.bitmap.get_height(): continue
                self.collision_mask[x_pos + y * self.bitmap.get_width()] = False
                self.bitmap.set_at((x_pos, y), (0, 0, 0, 0))

        self.update_cache()

    def update_cache(self):
        self.cached_texture = pygame.transform.scale(self.bitmap, (m.meters_to_pixels(self.size.x), m.meters_to_pixels(self.size.y)))

    def update(self):
        if g.zoom_changed:
            print("zoom changed")
            self.update_cache()

    def draw(self):
        gr.draw_sprite(self.cached_texture, pygame.Vector2(0.0, 0.0))
        # gr.draw_sprite_scale(self.bitmap, (0.0, 0.0, self.size.x, self.size.y))

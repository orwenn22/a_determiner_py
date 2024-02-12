import pyray

from engine import graphics as gr, metrics as m, globals as g
import math


class Terrain(object):
    def __init__(self, sprite: pyray.Texture, size: pyray.Vector2):
        self.size = size

    def check_collision(self, position: pyray.Vector2):
        """

        position: position in meter
        """
        print("TODO : implement check_collision")
        return False

    def check_collision_rec(self, rectangle: tuple[float, float, float, float]):
        """

        rectangle: hitbox in meter we want to check collision for
        """
        print("TODO : implement check_collision_rec")
        return False

    def destroy_rectangle(self, rectangle: tuple[float, float, float, float]):
        print("TODO : implement destroy_rectangle")

    def destroy_circle(self, center: pyray.Vector2, radius: float):
        print("TODO : implement destroy_circle")

    def destroy_circle_pixel(self, center: pyray.Vector2, radius_pixel: int):
        print("TODO : destroy_circle_pixel")

    def pixel_width(self) -> float:
        # return self.size.x / self.bitmap.get_width()
        print("TODO : pixel_width")
        return 0.0

    def pixel_height(self) -> float:
        # return self.size.y / self.bitmap.get_height()
        print("TODO : pixel_height")
        return 0.0

    def update(self):
        pass

    def draw(self):
        pass
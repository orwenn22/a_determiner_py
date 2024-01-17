import pygame
import math

from engine import globals as g, graphics as gr
from engine.object import kinematicobject as ko

class TestObj(ko.KinematicObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1, 10)
        self.throw_angle = 0.0
        self.strength = 100     # this is the launch force intensity in newton

    def update(self):
        self.throw_angle += (g.is_key_down(pygame.K_d) - g.is_key_down(pygame.K_q)) * g.deltatime

        if g.is_key_pressed(pygame.K_SPACE):
            # Here we need to divide by dt so it cancels with the dt from the velocity calculation (?)
            # this will result in adding a velocity of 5 meter / sec on this frame
            # self.apply_force(pygame.math.Vector2(5 * self.mass / g.deltatime, -5 * self.mass / g.deltatime))

            # Concept : we could say that each worms have a different strength when throwing an item. Therefore we could do it like this :
            self.apply_force(pygame.math.Vector2(math.cos(self.throw_angle), math.sin(self.throw_angle)) * self.strength / g.deltatime)
            # For now we just throw the box in the selected angle, but in the future we will spawn another object, then launch it like this :
            # throwed_item.apply_force(pygame.math.Vector2(self.strength * cos(throw_angle) / g.deltatime, self.strength * sin(throw_angle) / g.deltatime))

            self.enable_physics = True

    def draw(self):
        x, y, w, h = self.get_rectangle()
        gr.draw_rectangle(x, y, w, h, (255, 255, 255))

        self.draw_hitbox()  # debuggging

        # Throw angle
        gr.draw_line(
            self.position,
            self.position + pygame.math.Vector2(math.cos(self.throw_angle) * 1, math.sin(self.throw_angle) * 1),
            (0, 255, 255)
        )

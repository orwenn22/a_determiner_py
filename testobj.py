import pygame

from engine import globals as g, graphics as gr
from engine.object import kinematicobject as ko

class TestObj(ko.KinematicObject):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 1, 10)

    def update(self):
        if g.is_key_pressed(pygame.K_SPACE):
            # self.velocity.x = 500
            # self.velocity.y = -500

            # Here we need to devide by dt so it cancels with the dt from the velocity calculation (?)
            # this will result in adding a velocity of 5 meter / sec on this frame
            self.apply_force(pygame.math.Vector2(5 * self.mass / g.deltatime,
                                                 -5 * self.mass / g.deltatime))

            # Concept : we could say that each worms have a different strength when throwing an item. Therefore we could do it like this :
            # self.apply_force(pygame.math.Vector2(self.strength * cos(throw_angle) / g.deltatime, self.strength * sin(throw_angle) / g.deltatime))

            self.enable_physics = True

        # self.velocity.x = ((g.is_key_down(pygame.K_RIGHT) - g.is_key_down(pygame.K_LEFT))) * 100
        # self.velocity.y = ((g.is_key_down(pygame.K_DOWN) - g.is_key_down(pygame.K_UP))) * 100

    def draw(self):
        x, y, w, h = self.get_rectangle()
        gr.draw_rectangle(x, y, w, h, (255, 255, 255))
        self.draw_hitbox()

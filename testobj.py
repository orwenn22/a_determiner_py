import pygame

import globals as g

class TestObj(object):
    def __init__(self, x, y):
        self.mass = 10      # in kg
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, 0)
        self.enable_physics = False

        # self.velocity.x = 3000
        # self.velocity.y = -3000
        # self.acceleration.x = 100

    def update(self):
        if g.is_key_pressed(pygame.K_SPACE):
            # self.velocity.x = 500
            # self.velocity.y = -500

            # Here we need to devide by dt so it cancels with the dt from the velocity calculation (?)
            self.apply_force(pygame.math.Vector2(500 * self.mass / g.deltatime, -500 * self.mass / g.deltatime))    # this will result in adding a velocity of 500 pixels sec on this frame

            # Concept : we could say that each worms have a different strength when throwing an item. Therefore we could do it like this :
            # self.apply_force(pygame.math.Vector2(self.strength * cos(throw_angle) / g.deltatime, self.strength * sin(throw_angle) / g.deltatime))

            # self.apply_force(pygame.math.Vector2(0, -50000 * self.mass))
            self.enable_physics = True

        # self.velocity.x = ((g.is_key_down(pygame.K_RIGHT) - g.is_key_down(pygame.K_LEFT))) * 100
        # self.velocity.y = ((g.is_key_down(pygame.K_DOWN) - g.is_key_down(pygame.K_UP))) * 100

    def process_physics(self, dt: float):
        if not self.enable_physics:
            return

        # F = m * a
        self.apply_force(pygame.math.Vector2(0, 981*self.mass))     # gravity : 9.81 m/s² (assume 100 pixels is 1 meter)
        # self.acceleration.y = 981
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.acceleration = pygame.math.Vector2(0, 0)       # reset acceleration



    def apply_force(self, force: pygame.math.Vector2):
        # F = m * a <=> a = F/m
        new_acceleration = pygame.math.Vector2(force.x/self.mass, force.y/self.mass)
        self.acceleration += new_acceleration

    def draw(self):
        g.window.fill((255, 255, 255), (self.position.x, self.position.y, 60, 60))
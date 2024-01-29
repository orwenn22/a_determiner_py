import pygame

from . import entityobject as entityobject
from engine import graphics as gr


class KinematicObject(entityobject.EntityObject):
    def __init__(self, x: float, y: float, width: float, height: float, mass: float, spite: pygame.Surface = None):
        super().__init__(x, y, width, height, spite)
        self.velocity = pygame.math.Vector2(0, 0)       # velocity in m/s
        self.acceleration = pygame.math.Vector2(0, 0)   # acceleration in m/s²
        self.enable_physics = True                      # physics disabled by default
        self.enable_gravity = True                      # gravity enabled by default
        self.mass = mass                                # mass in kg
        # TODO : option to disable acceleration reset ?

    def process_physics_x(self, dt: float):
        if not self.enable_physics:
            return

        # TODO : if we add support for non-standard gravities, maybe there would be an horizontal gravity. If so, we should apply its force here.
        # if self.enable_gravity:
        #     self.apply_force(pygame.math.Vector2(some_force*self.mass, 0))
        self.velocity.x += self.acceleration.x * dt
        self.position.x += self.velocity.x * dt
        self.acceleration.x = 0.0

    def process_physics_y(self, dt: float):
        if not self.enable_physics:
            return

        if self.enable_gravity:
            self.apply_force(pygame.math.Vector2(0, 9.81*self.mass))
        self.velocity.y += self.acceleration.y * dt
        self.position.y += self.velocity.y * dt
        self.acceleration.y = 0.0

    def process_physics(self, dt: float):
        self.process_physics_x(dt)
        self.process_physics_y(dt)

    def process_physics_old(self, dt: float):
        """
        This is the original, kept for reference because we know it is working
        """
        if not self.enable_physics:
            return
        # F = m * a
        if self.enable_gravity:
            self.apply_force(pygame.math.Vector2(0, 9.81*self.mass))     # gravity : 9.81 m/s²
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
        self.acceleration = pygame.math.Vector2(0, 0)       # reset acceleration

    def apply_force(self, force: pygame.math.Vector2):
        # F = m * a <=> a = F/m
        new_acceleration = pygame.math.Vector2(force.x, force.y) / self.mass
        self.acceleration += new_acceleration

    def draw_hitbox(self):
        """
        This is intended for debugging purposes : draw the hitbox in red (maybe chose another color ?) and the velocity in yellow
        """
        super().draw_hitbox()

        # Velocity vector
        gr.draw_line(
            pygame.math.Vector2(self.position.x, self.position.y),
            pygame.math.Vector2(self.position.x, self.position.y) + self.velocity,
            (255, 255, 0)
        )

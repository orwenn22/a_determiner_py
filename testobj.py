import pygame
import math

from engine import globals as g, graphics as gr
from engine.object import kinematicobject as ko, kinematicprediction as kinematicprediction
from engine.state import state


class TestObj(ko.KinematicObject):
    def __init__(self, x, y, parent_state: state.State, mass=10):
        import gameplaystate
        super().__init__(x, y, 1, 1, mass)
        self.throw_angle = 0.0
        # this is the launch force intensity in newton (not really in reality, but we will pretend it is)
        self.strength = 100
        self.enable_physics = False
        self.parent_state: gameplaystate.GameplayState = parent_state

    def update(self, dt: float):
        self.throw_angle += (g.is_key_down(pygame.K_d) - g.is_key_down(pygame.K_q)) * g.deltatime

        if g.is_key_pressed(pygame.K_SPACE):
            # Here we need to divide by dt so it cancels with the dt from the velocity calculation (?)
            # this will result in adding a velocity of 5 meter / sec on this frame
            # self.apply_force(pygame.math.Vector2(5 * self.mass / dt, -5 * self.mass / dt))

            # Concept : we could say that each worms have a different strength when throwing an item. Therefore we could do it like this :
            self.apply_force(pygame.math.Vector2(math.cos(self.throw_angle), math.sin(self.throw_angle)) * self.strength / dt)
            # For now we just throw the box in the selected angle, but in the future we will spawn another object, then launch it like this :
            # throwed_item.apply_force(pygame.math.Vector2(self.strength * cos(throw_angle) / g.deltatime, self.strength * sin(throw_angle) / dt))

            self.enable_physics = True

        self.process_physics_x(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle()):
            while self.parent_state.t.check_collision_rec(self.get_rectangle()):
                self.position.x -= math.copysign(self.parent_state.t.pixel_width()/4, self.velocity.x)
            self.velocity.x = 0

        self.process_physics_y(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle()):
            # TODO : more complex collision checking for handling correctly slopes & other wierd terrain irregularities.
            while self.parent_state.t.check_collision_rec(self.get_rectangle()):
                self.position.y -= math.copysign(self.parent_state.t.pixel_height()/4, self.velocity.y)
            self.velocity.x = 0
            self.velocity.y = 0
            # We disable the physics once we have landed on the ground.
            # In the future we might want to call something in the state to pass the turn to the next player.
            self.enable_physics = False

        # if len(self.manager.get_collision(self, TestObj)) >= 1:
        #     print("collision detected")

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

        # Simulate throwing, and show trajectory
        # a = kinematicprediction.TestObjPrediction(self.position.x, self.position.y, self.width, self.height, self.mass, self.velocity)
        a = kinematicprediction.KinematicPrediction.from_other_object(self)

        # Add throwing force
        # And simulate with dt of 0.01
        a.apply_force(pygame.math.Vector2(math.cos(self.throw_angle), math.sin(self.throw_angle)) * self.strength / (0.01))
        a.draw_simulation(10)

import pyray
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
        self.throw_angle += (g.is_key_down(pyray.KeyboardKey.KEY_D) - g.is_key_down(pyray.KeyboardKey.KEY_Q)) * g.deltatime

        if g.is_key_pressed(pyray.KeyboardKey.KEY_SPACE):
            # Here we need to divide by dt so it cancels with the dt from the velocity calculation (?)
            # this will result in adding a velocity of 5 meter / sec on this frame
            # self.apply_force(pygame.math.Vector2(5 * self.mass / dt, -5 * self.mass / dt))

            # Concept : we could say that each worms have a different strength when throwing an item. Therefore we could do it like this :
            self.apply_force(pyray.Vector2(math.cos(self.throw_angle) * self.strength / dt,
                                           math.sin(self.throw_angle) * self.strength / dt))
            # For now we just throw the box in the selected angle, but in the future we will spawn another object, then launch it like this :
            # throwed_item.apply_force(pygame.math.Vector2(self.strength * cos(throw_angle) / g.deltatime, self.strength * sin(throw_angle) / dt))

            self.enable_physics = True
            self.width = 0.8
            self.height = 0.8

        self.process_physics_x(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle()):
            self.width = 1
            self.height = 1
            while self.parent_state.t.check_collision_rec(self.get_rectangle()):
                self.position.x -= math.copysign(self.parent_state.t.pixel_width()/2, self.velocity.x)
            self.velocity.x = 0

        self.process_physics_y(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle()):
            self.width = 1
            self.height = 1
            # TODO : more complex collision checking for handling correctly slopes & other wierd terrain irregularities.
            while self.parent_state.t.check_collision_rec(self.get_rectangle()):
                self.position.y -= math.copysign(self.parent_state.t.pixel_height()/2, self.velocity.y)

            if self.velocity.y > 0:     # going down (collision with ground)
                self.velocity.x = 0
                # We disable the physics once we have landed on the ground.
                # In the future we might want to call something in the state to pass the turn to the next player.
                self.enable_physics = False

            self.velocity.y = 0     # always reset y velocity on vertical collision

        # if len(self.manager.get_collision(self, TestObj)) >= 1:
        #     print("collision detected")

    def draw(self):
        gr.draw_rectangle(self.position.x - 0.5,
                          self.position.y - 0.5,
                          1, 1,
                          (255, 255, 255, 255))

        self.draw_hitbox()  # debuggging

        # Throw angle
        gr.draw_line(
            self.position,
            pyray.vector2_add(self.position, pyray.Vector2(math.cos(self.throw_angle) * 1, math.sin(self.throw_angle) * 1)),
            (0, 255, 255, 255)
        )

        # Simulate throwing, and show trajectory
        # a = kinematicprediction.TestObjPrediction(self.position.x, self.position.y, self.width, self.height, self.mass, self.velocity)
        a = kinematicprediction.KinematicPrediction.from_other_object(self)

        # Add throwing force
        # And simulate with dt of 0.01
        a.apply_force(pyray.Vector2(math.cos(self.throw_angle) * self.strength / 0.01,
                                    math.sin(self.throw_angle) * self.strength / 0.01))
        a.draw_simulation(10)

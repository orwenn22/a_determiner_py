import pyray
import math

from engine import globals as g, graphics as gr
from engine.object import kinematicobject as ko, kinematicprediction as kinematicprediction
from engine.widget import button, widget
from engine.state import state

import bullet


class TestObj(ko.KinematicObject):
    def __init__(self, x, y, team: int, parent_state: state.State, mass=10):
        """
        :param x: x position of the player
        :param y: y position of the player
        :param team: 0 for blue, 1 for red
        :param parent_state: parent state of the object
        :param mass: mass of the player
        """
        import gameplaystate
        super().__init__(x, y, 1, 1, mass)
        self.team = team
        self.throw_angle = 0.0
        # this is the launch force intensity in newton (not really in reality, but we will pretend it is)
        self.strength = 100
        self.enable_physics = False
        self.parent_state: gameplaystate.GameplayState = parent_state

        # This determine what the object is currently doing.
        # 0 : nothing, this is not this object's turn.
        # 1 : nothing, but this is this object's turn.
        # 2 : aiming to jump
        # 3 : aiming to shoot
        self.action = 0
        self.action_points = 20

        self.use_small_hitbox = False

    def update(self, dt: float):
        self.update_idle(dt)
        if self.action == 2:      # aiming to jump
            self.update_aim_to_jump(dt)
        elif self.action == 3:
            self.update_aim_to_shoot(dt)

        self.update_physics(dt)

    def draw(self):
        # TODO : replace with player sprite
        gr.draw_rectangle(self.position.x - 0.5,
                          self.position.y - 0.5,
                          1, 1,
                          (0, 0, 255, 255) if self.team == 0 else (255, 0, 0, 255))

        self.draw_hitbox()  # debuggging

        # Throw angle
        gr.draw_line(
            self.position,
            pyray.vector2_add(self.position, pyray.Vector2(math.cos(self.throw_angle) * 1, math.sin(self.throw_angle) * 1)),
            (0, 255, 255, 255)
        )

        if self.action == 2:
            a = kinematicprediction.KinematicPrediction.from_other_object(self)
            a.apply_force(pyray.Vector2(math.cos(self.throw_angle) * self.strength / 0.01,
                                        math.sin(self.throw_angle) * self.strength / 0.01))
            a.draw_simulation(10)
        elif self.action == 3:
            b = bullet.Bullet(self.position.x, self.position.y, self.parent_state)
            a = kinematicprediction.KinematicPrediction.from_other_object(b)
            a.apply_force(pyray.Vector2(math.cos(self.throw_angle) * self.strength / 0.01,
                                        math.sin(self.throw_angle) * self.strength / 0.01))
            a.draw_simulation(10)



    def update_idle(self, dt: float):
        """
        This always get executed, even when it is not the current player playing or if the action mode is set.
        """
        if not self.grounded():
            self.enable_physics = True

    def update_aim_to_jump(self, dt: float):
        """
        Mode 2 : the player is currently aiming for its next jump
        """
        self.throw_angle += (g.is_key_down(pyray.KeyboardKey.KEY_D) - g.is_key_down(pyray.KeyboardKey.KEY_Q)) * dt
        if g.is_key_pressed(pyray.KeyboardKey.KEY_SPACE) and self.action_points >= 20:
            self.action_points -= 20
            self.apply_force(pyray.Vector2(math.cos(self.throw_angle) * self.strength / dt,
                                           math.sin(self.throw_angle) * self.strength / dt))
            self.enable_physics = True
            self.use_small_hitbox = True
            self.action = 1
            self.parent_state.actions_widgets.clear()

    def update_aim_to_shoot(self, dt: float):
        """
        Mode 3 : the player is currently aiming for its shot
        """
        self.throw_angle += (g.is_key_down(pyray.KeyboardKey.KEY_D) - g.is_key_down(pyray.KeyboardKey.KEY_Q)) * dt
        if g.is_key_pressed(pyray.KeyboardKey.KEY_SPACE) and self.action_points >= 25:
            b = bullet.Bullet(self.position.x, self.position.y, self.parent_state)
            b.apply_force(pyray.Vector2(math.cos(self.throw_angle) * self.strength / dt,
                                        math.sin(self.throw_angle) * self.strength / dt))
            self.manager.add_object(b)
            self.action_points -= 25

    def update_physics(self, dt: float) -> None:
        """
        This update the physics of the player and checks for collisions.
        """
        # Horizontal
        self.process_physics_x(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True):
            self.use_small_hitbox = False
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True):
                self.position.x -= math.copysign(self.parent_state.t.pixel_width() / 2, self.velocity.x)
            self.velocity.x = 0

        # Vertical
        self.process_physics_y(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True):
            self.use_small_hitbox = False
            # TODO : more complex collision checking for handling correctly slopes & other wierd terrain irregularities.
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True):
                self.position.y -= math.copysign(self.parent_state.t.pixel_height() / 2, self.velocity.y)

            if self.velocity.y > 0:  # going down (collision with ground)
                self.velocity.x = 0
                # We disable the physics once we have landed on the ground.
                # In the future we might want to call something in the state to pass the turn to the next player.
                self.enable_physics = False
                if self.action == 1:
                    self.parent_state.show_action_widgets()

            self.velocity.y = 0  # always reset y velocity on vertical collision

        # if len(self.manager.get_collision(self, TestObj)) >= 1:
        #     print("collision detected")

    def get_action_widgets(self) -> list[widget.Widget]:
        def local_setaction_jump():
            self.action = 2

        def local_setaction_shoot():
            self.action = 3

        def local_skip_turn():
            self.action_points += 10
            self.parent_state.next_player_turn()

        button_size = 64
        result = []
        # We don't need to set the positions here because they are calculated in GameplayState.show_action_widgets()
        result.append(button.Button(0, 0, button_size, button_size, "BC", local_setaction_jump, "JUMP"))
        result.append(button.Button(0, 0, button_size*2, button_size, "BC", local_setaction_shoot, "SHOOT"))
        result.append(button.Button(0, 0, button_size, button_size, "BC", local_skip_turn, "SKIP"))
        return result

    def get_rectangle(self) -> tuple[float, float, float, float]:
        if not self.use_small_hitbox:
            return super().get_rectangle()
        else:
            old_w, old_h = self.width, self.height
            self.width *= 0.8
            self.height *= 0.8
            result = super().get_rectangle()
            self.width, self.height = old_w, old_h
            return result

    def grounded(self) -> bool:
        """
        This is not reliable for when we need extremely accurate collisions.
        It is meant to be used to detect if the floor below the player was updated while its physics is disabled,
        so we can re-enable it.
        """
        old_y = self.position.y
        self.position.y += 0.1
        result = self.parent_state.t.check_collision_rec(self.get_rectangle(), True)
        self.position.y = old_y
        return result

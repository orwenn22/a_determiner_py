import pyray
import math

from engine import graphics as gr
from engine.object import kinematicobject as ko
from engine.widget import button, widget


class Player(ko.KinematicObject):
    def __init__(self, x, y, team: int, parent_state, mass=10):
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

        # This determines what this player is currently playing.
        # 0 : it's not this object's turn.
        # 1 : it's this object's turn.
        self.is_playing = 0

        # Contain all the actions the player can do
        from playeraction import playeraction, jumpaction, shootaction
        self.actions: list[playeraction.PlayerAction] = [jumpaction.JumpAction(), shootaction.ShootAction()]
        self.current_action = -1

        # Some actions cost points. The points are stored in this.
        self.action_points = 20

        self.use_small_hitbox = False

    def update(self, dt: float):
        if not self.grounded():
            self.enable_physics = True

        if self.current_action >= 0:
            self.actions[self.current_action].on_update(self, dt)

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
            pyray.vector2_add(self.position, pyray.Vector2(
                math.cos(self.throw_angle) * 1, math.sin(self.throw_angle) * 1)),
            (0, 255, 255, 255)
        )

        if self.current_action >= 0:
            self.actions[self.current_action].on_draw(self)

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
                if self.is_playing == 1:
                    self.parent_state.show_action_widgets()

            self.velocity.y = 0  # always reset y velocity on vertical collision

        # if len(self.manager.get_collision(self, Player)) >= 1:
        #     print("collision detected")

    def get_action_widgets(self) -> list[widget.Widget]:
        button_size = 64
        result = []

        # We don't need to set the positions of the widgets here because they
        # are calculated in GameplayState.show_action_widgets()

        # Create a button for each actions
        for i in range(len(self.actions)):
            action_name = self.actions[i].action_name
            result.append(button.Button(0, 0, button_size, button_size,
                          "BC", self.make_action_callback(i), action_name))

        # Add the skip button
        def local_skip_turn():
            self.action_points += 10                # Increase points
            self.current_action = -1                # Cancel any action
            self.parent_state.next_player_turn()    # Give the turn to the next character (will clear action widgets)
        result.append(button.Button(0, 0, button_size, button_size, "BC", local_skip_turn, "Skip\n(0)"))
        return result

    def make_action_callback(self, index: int):
        """
        Creates a callback that will trigger the action's onclick
        """
        assert 0 <= index < len(self.actions), "Player : trying to create a callback to an action that does not exit !"

        def local_action_onclick():  # create the callback (the index variable is kept in the scope of this function)
            self.actions[index].on_click(self, index)
        return local_action_onclick  # return it

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

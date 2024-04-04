import pyray
import math

from engine import graphics as gr
from engine.object import kinematicobject as ko
from engine.widget import widget
from gameobject import wall
from widgets import actionbutton, fakeactionbutton
import globalresources as res


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

        self.solid_types = [wall.Wall]

        # This can be set to true by the current action in case we need to draw a custom sprite
        self.block_default_sprite = False

    def update(self, dt: float):
        if not self.grounded():
            self.enable_physics = True

        if 0 <= self.current_action < len(self.actions):
            self.actions[self.current_action].on_update(self, dt)

        self.update_physics(dt)

    def draw(self):
        self.block_default_sprite = False

        # Throw angle  TODO : remove this (or put this
        gr.draw_line(
            self.position,
            pyray.vector2_add(self.position, pyray.Vector2(
                math.cos(self.throw_angle) * 1, math.sin(self.throw_angle) * 1)),
            (0, 255, 255, 255)
        )

        # Draw action (this can set block_default_sprite to True)
        if 0 <= self.current_action < len(self.actions):
            self.actions[self.current_action].on_draw(self)

        # Player sprite
        if not self.block_default_sprite:
            if self.enable_physics:
                injump_sprite = res.player_in_jump_blue_sprite if self.team == 0 else res.player_in_jump_red_sprite
                flip_factor = -1 if self.velocity.x < 0 else 1
                gr.draw_sprite_rot_ex(injump_sprite,
                                      pyray.Rectangle(0, 0, flip_factor*injump_sprite.width, injump_sprite.height),
                                      pyray.Vector2(self.position.x, self.position.y + 0.15625/2),
                                      pyray.Vector2(1.0, 1.15625),      # 37/32 = 1.5625 (from size of sprite in pixe)
                                      0.0)
            else:
                player_sprite = res.player_blue_sprite if self.team == 0 else res.player_red_sprite
                gr.draw_sprite_rot_ex(player_sprite,
                                      pyray.Rectangle(0, 0, player_sprite.width, player_sprite.height),
                                      self.position,
                                      pyray.Vector2(1.0, 1.0),
                                      0.0)

        self.draw_hitbox()  # debuggging  TODO : remove this

    def update_physics(self, dt: float) -> None:
        """
        This update the physics of the player and checks for collisions.
        """
        # Horizontal
        self.process_physics_x(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
            self.use_small_hitbox = False
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
                 #self.position.x -= math.copysign(self.parent_state.t.pixel_width() / 2, self.velocity.x)
                 self.position.x -= math.copysign(0.01, self.velocity.x)
            self.velocity.x = 0

        # Vertical
        self.process_physics_y(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
            self.use_small_hitbox = False
            # TODO : more complex collision checking for handling correctly slopes & other wierd terrain irregularities.
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
                #self.position.y -= math.copysign(self.parent_state.t.pixel_height() / 2, self.velocity.y)
                self.position.y -= math.copysign(0.01, self.velocity.y)

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
        result = []

        # Create a button for each actions
        for i in range(len(self.actions)):
            result.append(actionbutton.ActionButton(self, i))

        # Add the skip button
        def local_skip_turn():
            self.action_points += 10                # Increase points
            self.current_action = -1                # Cancel any action
            self.parent_state.next_player_turn()    # Give the turn to the next character (will clear action widgets)

        skip_button = fakeactionbutton.FakeActionButton("Skip", "(+10)", local_skip_turn)
        result.append(skip_button)
        return result

    def add_action(self, action):
        # TODO : assertion if action is not an action ?
        self.actions.append(action)
        if self.parent_state.show_actions and self.parent_state.players[self.parent_state.current_player] == self:
            self.parent_state.show_action_widgets()    # refresh

    def remove_action(self, action):
        """
        Intended for actions with limited use, so they can remove themselves.
        """
        if action not in self.actions:
            return

        self.actions.remove(action)
        if self.parent_state.show_actions and self.parent_state.players[self.parent_state.current_player] == self:
            self.parent_state.show_action_widgets()  # refresh

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
        self.position.y += 0.02
        result = self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object()
        self.position.y = old_y
        return result

    def collide_with_solid_object(self) -> bool:
        for solid in self.solid_types:
            col = self.manager.get_collision(self, solid)
            if len(col) >= 1:
                return True
        return False

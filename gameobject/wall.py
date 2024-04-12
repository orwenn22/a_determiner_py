from gameobject import player
from engine.object import kinematicobject
import globalresources as ges
from engine import graphics
import math
import engine.utils as utils


class Wall(kinematicobject.KinematicObject):
    def __init__(self, x: float, y: float, width: float, height: float, parent_state):
        sprite = ges.wall_sprite

        super().__init__(x, y, width, height, 50, sprite)
        self.parent_state = parent_state

        self.solid_types = [Wall]

    def update(self, dt: float):
        self.update_physics(dt)

        if not self.is_grounded():
            self.enable_physics = True

    def draw(self):
        graphics.draw_sprite_scale(self.sprite, self.get_rectangle())

    def update_physics(self, dt: float):
        # Horizontal
        self.process_physics_x(dt)

        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        for p in cols:
            # Make ture the player fall if it is pushed in the void by the wall
            p.enable_physics = True

            # Shift the player in the opposite direction
            while utils.check_collision_rectangles(self.get_rectangle(), p.get_rectangle()):
                p.position.x += math.copysign(0.02, self.velocity.x)

            # After pushing the player, if we are on a slope, it is possible that it is clipping in the floor,
            # so move it up if it is the case
            it = 0          # (it = iterations)
            while self.parent_state.t.check_collision_rec(p.get_rectangle()) and it <= 20:
                p.position.y -= self.parent_state.t.pixel_height() / 2      # maybe this needs to be replaced by 0.02 ?
                it += 1

            # Crushed by wall and terrain
            if self.parent_state.t.check_collision_rec(p.get_rectangle()) or p.collide_with_solid_object():
                self.parent_state.kill_player(p)
                continue        # just in case wa add more stuff in the future :)

        # If the wall itself if colliding with the terrain or another solid object then we shift it
        # to the opposite direction
        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
                self.position.x -= math.copysign(self.parent_state.t.pixel_width() / 2, self.velocity.x)
            self.velocity.x = 0

        # Vertical
        self.process_physics_y(dt)

        # If the wall crush players then we need to kill them.
        # If the player is on the wall however, we need to move it with the wall. | TODO : stress test this
        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        for p in cols:
            if self.velocity.y > 0:     # going down
                p.parent_state.kill_player(p)
            else:                       # going up
                p.velocity.y = self.velocity.y
                p.velocity.x = self.velocity.x      # maybe ???
                p.enable_physics = True

        # If the wall is clipping with the terrain then we make it go in the opposite direction of its velocity
        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
                #self.position.y -= math.copysign(self.parent_state.t.pixel_height() / 2, self.velocity.y)
                self.position.y -= math.copysign(0.01, self.velocity.y)

            if self.velocity.y > 0:  # going down (collision with ground)
                self.velocity.x = 0
                self.enable_physics = False
            self.velocity.y = 0

    def is_grounded(self) -> bool:
        old_y = self.position.y
        self.position.y += 0.01
        result = self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object()
        self.position.y = old_y
        return result

    def collide_with_solid_object(self) -> bool:
        if self.manager is None:
            return False

        for solid in self.solid_types:
            col = self.manager.get_collision(self, solid)
            if len(col) >= 1:
                return True
        return False

import player
from engine.object import kinematicobject
import globalresources as ges
from engine import graphics
import math


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
            p.velocity.x = self.velocity.x
            p.enable_physics = True
            p.use_small_hitbox = True       # ????

            # the thing below is currently broken
            """# Backup current pos and simulate one tick of physics
            old_player_pos = pyray.Vector2(p.position.x, p.position.y)
            p.position.x += p.velocity.x * dt
            p.position.y += p.velocity.y * dt
            if self.parent_state.t.check_collision_rec(p.get_rectangle()) or p.collide_with_solid_object():      # Crushed by wall and terrain
                self.parent_state.kill_player(p)
                continue

            # Restore backup (we don't restore the
            p.position = pyray.Vector2(old_player_pos.x, old_player_pos.y)"""

        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
                self.position.x -= math.copysign(self.parent_state.t.pixel_width() / 2, self.velocity.x)
            self.velocity.x = 0

        # Vertical
        self.process_physics_y(dt)

        # If the wall crush players then we need to kill them
        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        for p in cols:
            if self.velocity.y > 0:     # going down
                p.parent_state.kill_player(p)
            else:                       # going up
                p.velocity.y = self.velocity.y
                p.velocity.x = self.velocity.x      # ???
                p.enable_physics = True

        # If the wall is clipping with the terrain then we make it go back up
        if self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
            while self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object():
                self.position.y -= math.copysign(self.parent_state.t.pixel_height() / 2, self.velocity.y)

            if self.velocity.y > 0:  # going down (collision with ground)
                self.velocity.x = 0
                self.enable_physics = False
            self.velocity.y = 0

    def is_grounded(self) -> bool:
        old_y = self.position.y
        self.position.y += 0.01
        if self.manager is None:
            result = self.parent_state.t.check_collision_rec(self.get_rectangle())
        else:
            result = self.parent_state.t.check_collision_rec(self.get_rectangle(), True) or self.collide_with_solid_object()
        self.position.y = old_y
        return result

    def collide_with_solid_object(self) -> bool:
        for solid in self.solid_types:
            col = self.manager.get_collision(self, solid)
            if len(col) >= 1:
                return True
        return False

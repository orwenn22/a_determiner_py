import player
from engine.object import kinematicobject
import globalresources as ges
from engine import graphics
import terrain
import math

class Wall(kinematicobject.KinematicObject):
    def __init__(self, x: float, y: float, width: float, height: float, t: terrain.Terrain):
        sprite = ges.wall_sprite

        super().__init__(x, y, width, height, 10, sprite) # wall is really heavy and as such should fall really fast | it's false but this commentary will stay like that because it's fun
        self.grounded = False
        self.terrain = t

    def update(self, dt: float):
        # possible TODO: currently the wall don't have horizontal physics.

        # If the wall is not grounded then we need to make it fall
        if self.grounded is False: 
            self.process_physics_y(dt)

            # If the wall crush players then we need to kill them
            cols: list[player.Player] = self.manager.get_collision(self, player.Player)
            for p in cols:
                p.parent_state.kill_player(p)

            # If the wall is clipping with the terrain then we make it go back up
            while self.terrain.check_collision_rec(self.get_rectangle(), True):
                self.position.y -= 0.01
                self.velocity.y = 0
                self.grounded = True
        # Currently when the wall reaches the wall for the first time it will never fall again.
        # Maybe this shouldn't be the case ?
        # If so we should uncomment this :
        elif not self.is_grounded():
            self.grounded = False

        self.process_physics_x(dt)
        if self.terrain.check_collision_rec(self.get_rectangle(), True): 
            self.use_small_hitbox = False
            while self.terrain.check_collision_rec(self.get_rectangle(), True):
                self.position.x -= math.copysign(self.terrain.pixel_width() / 2, self.velocity.x)
            self.velocity.x = 0



    def draw(self):
        graphics.draw_sprite_scale(self.sprite, self.get_rectangle())

    def is_grounded(self) -> bool:
        old_y = self.position.y
        self.position.y += 0.01
        result = self.terrain.check_collision_rec(self.get_rectangle(), True)
        self.position.y = old_y
        return result

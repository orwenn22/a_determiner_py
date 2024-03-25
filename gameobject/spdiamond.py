import pyray
from engine.object import entityobject
import globalresources as res
from engine import graphics as gr
from . import player

class SPDiamond(entityobject.EntityObject):
    def __init__(self, x:float, y:float):
        super().__init__(x, y, 0.3, 0.5, res.spdiamond_sprite)       # change xpdiamond_sprite with jude battery sprite
        self.action_points = 25

    def update(self, dt: float):
        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        if len(cols) > 0:
            cols[0].action_points += self.action_points
            self.manager.remove_object(self)

    def draw(self):
        pyray.get_time()
        position = pyray.Vector2(self.position.x, self.position.y + int(pyray.get_time()%2)/20 )
        gr.draw_sprite_rot(self.sprite, position, pyray.Vector2(self.width, self.height), 0.0 )



import pyray
import globalresources as res
from engine import graphics as gr
from gameobject import player
from items import collectible


class SPDiamond(collectible.Collectible):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self._setup_collectible(0.3, 0.5, res.spdiamond_sprite)  # TODO change xpdiamond_sprite with jude battery sprite
        self.action_points = 25
        self.existence_time = 0

    def update(self, dt: float):
        self.existence_time += dt
        self.existence_time %= 2
        super().update(dt)

    def on_collect(self, p: player.Player) -> bool:
        p.action_points += self.action_points
        return True

    def draw(self):
        position = pyray.Vector2(self.position.x, self.position.y - int(self.existence_time)/20)
        gr.draw_sprite_rot(self.sprite, position, pyray.Vector2(self.height, self.height), 0.0)

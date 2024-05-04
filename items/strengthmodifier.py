import pyray

from engine import graphics as gr
from items import collectible
from gameobject import player
import globalresources as res


class StrengthModifier(collectible.Collectible):
    def __init__(self, x: float, y: float, points: int):
        super().__init__(x, y)
        super()._setup_collectible(0.5, 0.5, res.strength_downgrade_sprite if points < 0 else res.strength_upgrade_sprite)
        self.points = points
        self.existence_time = 0.0

    def update(self, dt: float):
        self.existence_time += dt
        self.existence_time %= 1.0

        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        for p in cols:
            if p.strength + self.points > 0:
                p.strength += self.points
                self.manager.remove_object(self)
                return

    def draw(self):
        position = pyray.Vector2(self.position.x, self.position.y - float(self.existence_time//0.5)*0.05)
        gr.draw_sprite_rot(self.sprite, position, pyray.Vector2(self.width, self.height), 0.0)

    @classmethod
    def make_upgrade(cls, x: float, y: float):
        return cls(x, y, 5)

    @classmethod
    def make_downgrade(cls, x: float, y: float):
        return cls(x, y, -5)

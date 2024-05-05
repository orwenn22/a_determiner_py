import pyray
from gameobject import player
from engine import graphics as gr
from playeraction import spawnwall 
import globalresources as res
from items import collectible


class Trowel(collectible.Collectible):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self._setup_collectible(0.6, 0.4, res.trowel_sprite)

    def on_collect(self, p: player.Player) -> bool:
        p.add_action(spawnwall.PlaceWallAction())
        return True

    def draw(self):
        gr.draw_sprite_rot(self.sprite, self.position, pyray.Vector2(self.width, self.height), 0.0)

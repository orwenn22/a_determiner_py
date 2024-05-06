import pyray

from gameobject import player
from playeraction import hotpotatoaction
from items import collectible
import globalresources as res
from engine import graphics as gr


class HotPotato(collectible.Collectible):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self._setup_collectible(0.5, 0.5, res.potato_sprite)

    def on_collect(self, p: player.Player) -> bool:
        # TODO : make it so the player can only carry one hot potato ?
        p.add_action(hotpotatoaction.HotPotatoAction())
        p.action_points += 10
        return True

    def draw(self):
        gr.draw_sprite_rot(self.sprite, self.position, pyray.Vector2(self.width, self.height), 0.0)

import pyray
from gameobject import player
from engine import graphics as gr
from playeraction import placeportalsaction
import globalresources as res
from items import collectible


class PortalGun(collectible.Collectible):
    def __init__(self, x: float, y: float):
        super().__init__(x, y)
        self._setup_collectible(0.6, 0.4, res.portal_gun_sprite)

    def update(self, dt: float):
        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        if len(cols) > 0:
            cols[0].add_action(placeportalsaction.PlacePortalsAction())
            self.manager.remove_object(self)

    def draw(self):
        gr.draw_sprite_rot(self.sprite, self.position, pyray.Vector2(self.width, self.height), 0.0)

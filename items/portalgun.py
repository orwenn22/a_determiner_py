import pyray
from objects import player
from engine.object import entityobject
from engine import graphics as gr
from playeraction import placeportalsaction
import globalresources as res


class PortalGun(entityobject.EntityObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 0.6, 0.4, res.portal_gun_sprite)

    def update(self, dt: float):
        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        if len(cols) > 0:
            cols[0].add_action(placeportalsaction.PlacePortalsAction())
            self.manager.remove_object(self)

    def draw(self):
        gr.draw_sprite_rot(self.sprite, self.position, pyray.Vector2(self.width, self.height), 0.0)

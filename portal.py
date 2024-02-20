import pyray

import bullet
import player
from engine import graphics as gr
from engine.object import entityobject, objectmanager


class Portal(entityobject.EntityObject):
    def __init__(self, x: float, y: float, sprite: pyray.Texture = None):
        super().__init__(x, y, 1.0, 1.0, sprite)
        self.destination: Portal | None = None
        self.whitelisted_types = [player.Player, bullet.Bullet]
        self.cooldown = 1.0

    def update(self, dt: float):
        if self.destination is None:
            return

        if self.cooldown > 0.0:
            self.cooldown -= dt
            return

        cols = self.manager.get_collision(self)
        for obj in cols:
            if type(obj) not in self.whitelisted_types: continue
            self.cooldown = 1.0
            self.destination.cooldown = 1.0
            obj.position.x = self.destination.position.x
            obj.position.y = self.destination.position.y

    def draw(self):
        if self.sprite is None:
            gr.draw_circle(self.position, self.width/2, (200, 122, 255, 127 if self.cooldown > 0 else 255))
        else:
            gr.draw_sprite_rot(self.sprite, self.position, pyray.Vector2(self.width, self.height), 0.0)
        pass

    def set_destination(self, destination):
        self.destination = destination

    @classmethod
    def spawn_portals(cls, manager: objectmanager.ObjectManager, x1: float, y1: float, x2: float, y2: float, sprite: pyray.Texture):
        p1 = cls(x1, y1, sprite)
        p2 = cls(x2, y2, sprite)
        p1.set_destination(p2)
        p2.set_destination(p1)
        manager.add_object(p1)
        manager.add_object(p2)

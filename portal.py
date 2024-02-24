import pyray

import bullet
import player
import wall
from engine import graphics as gr, globals as g, metrics as m, utils
from engine.object import entityobject, objectmanager


class Portal(entityobject.EntityObject):
    def __init__(self, x: float, y: float, sprite: pyray.Texture = None):
        super().__init__(x, y, 1.0, 1.0, sprite)
        self.destination: Portal | None = None
        self.whitelisted_types = [player.Player, bullet.Bullet, wall.Wall]
        self.cooldown = 1.0
        self.mouse_overing = False

    def update(self, dt: float):
        self.mouse_overing = False
        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
        mouse_meters = m.window_position_to_meters_position(mouse_x, mouse_y)

        if not g.mouse_used and utils.check_collision_point_rect((mouse_meters.x, mouse_meters.y), self.get_rectangle()):
            g.mouse_used = True
            self.mouse_overing = True

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

        # If there are no destination draw a red dot and stop drawing here
        if self.destination is None:
            gr.draw_circle(self.position, 0.05, (255, 0, 0, 255))
            return

        # Draw a line between this portal and its destinations if overed
        elif self.mouse_overing or self.destination.mouse_overing:
            vec_step = pyray.vector2_subtract(self.destination.position, self.position)
            vec_step = pyray.vector2_scale(vec_step, 1.0/15.0)
            painter_pos = pyray.Vector2(self.position.x, self.position.y)
            for i in range(15):
                gr.draw_circle(painter_pos, 0.05, (150, 92, 191, 255))
                painter_pos = pyray.vector2_add(painter_pos, vec_step)
            gr.draw_line(self.position, self.destination.position, (150, 92, 191, 255))

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

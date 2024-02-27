import pyray

from engine.object import entityobject
from engine import graphics as gr
import globalresources as res


class Explosion(entityobject.EntityObject):
    def __init__(self, x: float, y: float, radius: float):
        super().__init__(x, y, radius*2, radius*2, res.explosion_spritesheet)
        self.anim_timer = 0
        self.anim_duration = 1      # in second

    def update(self, dt: float):
        self.anim_timer += dt
        if self.anim_timer >= self.anim_duration:
            self.manager.remove_object(self)

    def draw(self):
        animation_frame = int((self.anim_timer / self.anim_duration) * 16)  # 16 frames in explosion animation

        gr.draw_sprite_rot_ex(self.sprite,
                              pyray.Rectangle(71*animation_frame, 0, 71, 98),
                              self.position,
                              pyray.Vector2(self.width*1.5, self.height*2.25),
                              0.0)

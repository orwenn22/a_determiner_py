import pyray

from engine.object import entityobject
from engine import graphics as gr
import globalresources as res


class Explosion(entityobject.EntityObject):
    def __init__(self, x: float, y: float, radius: float, parent_state):
        super().__init__(x, y, radius*2, radius*2, res.explosion_spritesheet)
        self.power = radius
        self.parent_state = parent_state
        self.anim_timer = 0
        self.anim_duration = 1      # in second
        self.exploded_terrain = False

    def update(self, dt: float):
        self.anim_timer += dt

        animation_frame = self.get_current_animation_frame()
        if animation_frame == 6:
            self.explode_terrain(dt)

        if self.anim_timer >= self.anim_duration:
            self.manager.remove_object(self)

    def draw(self):
        animation_frame = self.get_current_animation_frame()

        gr.draw_sprite_rot_ex(self.sprite,
                              pyray.Rectangle(71*animation_frame, 0, 71, 98),
                              self.position,
                              pyray.Vector2(self.width*1.5, self.height*2.25),
                              0.0)

    def explode_terrain(self, dt: float):
        """
        This function is what actually destroys the terrain (TODO : and in the future give kb to nearby objects)
        """
        if self.exploded_terrain:
            return
        self.exploded_terrain = True
        self.parent_state.t.destroy_circle(self.position, self.power)

    def get_current_animation_frame(self):
        return int((self.anim_timer / self.anim_duration) * 16)  # 16 frames in explosion animation
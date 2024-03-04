import math

import pyray

from engine.object import entityobject, kinematicobject as kinematicobject
from engine import graphics as gr
import globalresources as res


class Explosion(entityobject.EntityObject):
    def __init__(self, x: float, y: float, radius: float, parent_state):
        super().__init__(x, y, radius*2, radius*2, res.explosion_spritesheet)
        self.radius = radius         # This is the radius of the explosion
        self.explosion_power = 500   # used to calculate the force applied to nearby objects
        self.parent_state = parent_state
        self.anim_timer = 0
        self.anim_duration = 1      # in second
        self.exploded_terrain = False
        self.exploded_enemies = False
      
    def update(self, dt: float):
        self.anim_timer += dt
    
        # This is executed only once
        self.explode_nearby_enemies(dt)

        animation_frame = self.get_current_animation_frame()
        if animation_frame >= 6:
            self.explode_terrain()

        if self.anim_timer >= self.anim_duration:
            self.manager.remove_object(self)

    def draw(self):
        animation_frame = self.get_current_animation_frame()

        gr.draw_sprite_rot_ex(self.sprite,
                              pyray.Rectangle(71*animation_frame, 0, 71, 98),
                              self.position,
                              pyray.Vector2(self.width*1.5, self.height*2.25),
                              0.0)

    def explode_terrain(self):
        """
        This function is what actually destroys the terrain
        """
        if self.exploded_terrain:
            return
        self.exploded_terrain = True
        self.parent_state.t.destroy_circle(self.position, self.radius)

    def explode_nearby_enemies(self, dt: float):
        if self.exploded_enemies:
            return

        self.exploded_enemies = True
        for obj in self.manager.list_object:
            if isinstance(obj, kinematicobject.KinematicObject):
                self._apply_force_to_other(obj, dt)

    def _apply_force_to_other(self, obj: kinematicobject.KinematicObject, dt: float):
        relative_position = pyray.Vector2(obj.position.x - self.position.x, obj.position.y - self.position.y)
        distance = math.sqrt(relative_position.x**2 + relative_position.y**2)

        # The object is too far, we don't need to apply a force on it.
        if distance > self.radius:
            return

        # Calculate the coefficient we neet to apply to the force
        force_coefficient = 1 - distance/self.radius
        total_coefficient = force_coefficient*self.explosion_power

        # Calculate the vector of the force
        normalised_vector = pyray.vector2_normalize(relative_position)
        # total_force = pyray.Vector2(normalised_vector.x*total_coefficient/dt,
        #                             normalised_vector.y*total_coefficient/dt)
        total_force = pyray.vector2_scale(normalised_vector, total_coefficient/dt)
        print(total_force.x, total_force.y)
        obj.apply_force(total_force)
        # If the player is grounded, then its physics is disabled, which mean that if we don't enable it again,
        # the force will be processed when the ground is destroyed, which would cause the player to make a huuuge jump.
        # TODO ? : only do this for the player ??? idk
        obj.enable_physics = True

    def get_current_animation_frame(self):
        return int((self.anim_timer / self.anim_duration) * 16)  # 16 frames in explosion animation

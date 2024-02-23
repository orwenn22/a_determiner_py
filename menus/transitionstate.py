import pyray

from engine.state import state
import globalresources as res

class TransitonState(state.State):
    def __init__(self, old_state: state.State, new_state: state.State):
        self.anim_state = 0
        self.anim_timer = 0
        self.anim_duration = 1

        self.old_state = old_state
        self.new_state = new_state

        self.old_rt = pyray.load_render_texture(pyray.get_render_width(), pyray.get_render_height())
        self.new_rt = pyray.load_render_texture(pyray.get_render_width(), pyray.get_render_height())

        pyray.begin_texture_mode(self.old_rt)
        self.old_state.draw()
        pyray.end_texture_mode()

        pyray.begin_texture_mode(self.new_rt)
        self.new_state.draw()
        pyray.end_texture_mode()

    def unload_ressources(self):
        pyray.unload_render_texture(self.old_rt)
        pyray.unload_render_texture(self.new_rt)

    def update(self, dt: float):
        self.anim_timer += dt

        if self.anim_timer > self.anim_duration:
            self.anim_timer = 0
            self.anim_state += 1
            if self.anim_state >= 2:
                self.manager.set_state(self.new_state)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        delimitation_x = pyray.get_render_width() * ((self.anim_duration-self.anim_timer)/self.anim_duration)
        left_texture: pyray.Texture = None
        right_texture: pyray.Texture = None
        left_flip_factor = 1
        right_flip_factor = 1
        if self.anim_state == 0:
            left_texture = self.old_rt.texture
            right_texture = res.cool_transition_sprite
            left_flip_factor = -1
        else:
            left_texture = res.cool_transition_sprite
            right_texture = self.new_rt.texture
            right_flip_factor = -1
            pass

        pyray.draw_texture_pro(left_texture,
                               pyray.Rectangle(0, 0, left_texture.width, left_texture.height * left_flip_factor),
                               pyray.Rectangle(0, 0, delimitation_x, pyray.get_render_height()),
                               pyray.Vector2(0, 0), 0, pyray.WHITE)

        pyray.draw_texture_pro(right_texture,
                               pyray.Rectangle(0, 0, right_texture.width, right_texture.height * right_flip_factor),
                               pyray.Rectangle(delimitation_x, 0, pyray.get_render_width()-delimitation_x, pyray.get_render_height()),
                               pyray.Vector2(0, 0), 0, pyray.WHITE)

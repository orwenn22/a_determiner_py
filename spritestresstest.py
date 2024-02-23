from engine.state import state
from engine import graphics as gr, globals as g, metrics as m
import pyray


class SpriteStressTest(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit
        m.set_pixels_per_meter(50)

        # Put the cam at the center of the world
        m.set_camera_center(pyray.Vector2(0, 0))

        # This is the sprite for the stress test
        self.my_sprite = pyray.load_texture("res/testsprite.png")
        self.rot = 0.0

    def __del__(self):
        pyray.unload_texture(self.my_sprite)

    def update(self, dt: float):
        if g.is_key_pressed(pyray.KeyboardKey.KEY_T):
            import gameplaystate
            self.manager.set_state(gameplaystate.GameplayState())
            print(self)
            return

        # Move the camera at 5 meters / sec
        m.x_offset_pixel += -(g.is_key_down(pyray.KeyboardKey.KEY_RIGHT) -
                              g.is_key_down(pyray.KeyboardKey.KEY_LEFT)) * m.meters_to_pixels(5) * dt
        m.y_offset_pixel += -(g.is_key_down(pyray.KeyboardKey.KEY_DOWN) -
                              g.is_key_down(pyray.KeyboardKey.KEY_UP)) * m.meters_to_pixels(5) * dt

        self.rot += 4 * dt

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        gr.draw_grid()

        # Draw a HUUUGE sprite to see how much it reduces framerate
        # gr.draw_sprite_scale(self.my_sprite, (0, 0, 1920*5, 1080*5))

        # Uncomment stuff here to test features
        for i in range(0, 10000):
            # gr.draw_sprite_scale(self.my_sprite, (i, 0, float(10), float(10)))
            gr.draw_sprite_rot(self.my_sprite, pyray.Vector2(i, 0), pyray.Vector2(2, 1), self.rot)

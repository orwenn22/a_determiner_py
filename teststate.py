from engine.state import state
from engine.object import objectmanager
from engine import metrics as m, graphics as gr, globals as g
import pyray
import testobj


class TestState(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit
        m.set_pixels_per_meter(50)

        # Put the cam at the center of the world
        m.set_camera_center(pyray.Vector2(0, 0))

        # create a manager with some objects in it
        self.object_manager = objectmanager.ObjectManager()
        self.object_manager.add_object(testobj.TestObj(1, 1))
        self.object_manager.add_object(testobj.TestObj(3, 1, 20))

    def update(self, dt):
        if g.is_key_pressed(pyray.KeyboardKey.KEY_T):
            import spritestresstest
            self.manager.set_state(spritestresstest.SpriteStressTest())
            return

        # Move the camera at 5 meters / sec
        m.x_offset_pixel += -(g.is_key_down(pyray.KeyboardKey.KEY_RIGHT) -
                              g.is_key_down(pyray.KeyboardKey.KEY_LEFT)) * m.meters_to_pixels(5) * dt
        m.y_offset_pixel += -(g.is_key_down(pyray.KeyboardKey.KEY_DOWN) -
                              g.is_key_down(pyray.KeyboardKey.KEY_UP)) * m.meters_to_pixels(5) * dt

        # Zoom control
        if g.is_key_pressed(pyray.KeyboardKey.KEY_KP_ADD):
            m.set_pixels_per_meter(m.pixels_per_meter * 2)
        elif g.is_key_pressed(pyray.KeyboardKey.KEY_KP_SUBTRACT):
            m.set_pixels_per_meter(m.pixels_per_meter // 2)

        self.object_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        gr.draw_grid()
        self.object_manager.draw()

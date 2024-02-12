from engine.state import state
from engine.object import objectmanager
from engine import metrics as m, graphics as gr, globals as g
import pyray
import testobj
import terrain


class GameplayState(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit
        m.set_pixels_per_meter(50)

        # Put the cam at the center of the world
        m.set_camera_center(pyray.Vector2(0, 0))

        # create a manager with some objects in it
        self.object_manager = objectmanager.ObjectManager()
        self.object_manager.add_object(testobj.TestObj(1, 1, self))
        self.object_manager.add_object(testobj.TestObj(3, 1,  self, 20))

        self.terrain_surface = pyray.load_texture("level2.png")
        self.t = terrain.Terrain(self.terrain_surface, pyray.Vector2(25, 12))

        self.mouse_rec = (0, 0, 1, 1)

        self.cam_follow_mouse = False
        self.cam_mouse_offset = (0, 0)

    def __del__(self):
        pyray.unload_texture(self.terrain_surface)

    def update(self, dt):
        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()

        if g.is_key_pressed(pyray.KeyboardKey.KEY_T):
            import spritestresstest
            self.manager.set_state(spritestresstest.SpriteStressTest())
            return

        self.update_cam_position(mouse_x, mouse_y)

        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        self.mouse_rec = (mouse_pos_meter.x, mouse_pos_meter.y, 1.0, 1.0)

        # print(self.t.check_collision_rec(self.mouse_rec))
        if g.is_key_down(pyray.KeyboardKey.KEY_B):
            # self.t.destroy_rectangle(self.mouse_rec)
            self.t.destroy_circle(mouse_pos_meter, 1)

        self.t.update()

        self.object_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        self.t.draw()
        gr.draw_grid()
        gr.draw_rectangle(self.mouse_rec[0], self.mouse_rec[1], self.mouse_rec[2], self.mouse_rec[3], (255, 255, 0))
        self.object_manager.draw()

    def update_cam_position(self, mouse_x, mouse_y):
        # Drag & drop cam
        if g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_RIGHT):
            self.cam_follow_mouse = True
            self.cam_mouse_offset = (m.x_offset_pixel - mouse_x, m.y_offset_pixel - mouse_y)
        if not g.is_mouse_button_down(pyray.MouseButton.MOUSE_BUTTON_RIGHT):
            self.cam_follow_mouse = False
        if self.cam_follow_mouse:
            m.x_offset_pixel = self.cam_mouse_offset[0] + mouse_x
            m.y_offset_pixel = self.cam_mouse_offset[1] + mouse_y
        else:
            # Zoom (we can't zoom while dragging)
            cam_center = m.get_camera_center()
            if g.mouse_wheel > 0:
                m.set_pixels_per_meter(m.pixels_per_meter * 2)
            elif g.mouse_wheel < 0:
                m.set_pixels_per_meter(m.pixels_per_meter // 2)
            m.set_camera_center(cam_center)

        # Move the camera at 5 meters / sec
        # m.x_offset_pixel += -(g.is_key_down(pygame.K_RIGHT) -
        #                       g.is_key_down(pygame.K_LEFT)) * m.meters_to_pixels(5) * dt
        # m.y_offset_pixel += -(g.is_key_down(pygame.K_DOWN) -
        #                      g.is_key_down(pygame.K_UP)) * m.meters_to_pixels(5) * dt

        # Zoom control
        # if g.is_key_pressed(pygame.K_KP_PLUS):
        #     m.set_pixels_per_meter(m.pixels_per_meter * 2)
        # elif g.is_key_pressed(pygame.K_KP_MINUS):
        #     m.set_pixels_per_meter(m.pixels_per_meter // 2)

from engine.state import state
from engine.object import objectmanager
from engine import metrics as m, graphics as gr, globals as g
import pygame
import testobj
import terrain


class TestState(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit
        m.set_pixels_per_meter(50)

        # Put the cam at the center of the world
        m.set_camera_center(pygame.math.Vector2(0, 0))

        # create a manager with some objects in it
        self.object_manager = objectmanager.ObjectManager()
        self.object_manager.add_object(testobj.TestObj(1, 1))
        self.object_manager.add_object(testobj.TestObj(3, 1, 20))

        self.terrain_surface = pygame.image.load("level.png")
        self.t = terrain.Terrain(self.terrain_surface, pygame.Vector2(25, 12))

        self.mouse_rec = (0, 0, 1, 1)

    def update(self, dt):
        if g.is_key_pressed(pygame.K_t):
            import spritestresstest
            self.manager.set_state(spritestresstest.SpriteStressTest())
            return

        # Move the camera at 5 meters / sec
        m.x_offset_pixel += -(g.is_key_down(pygame.K_RIGHT) -
                              g.is_key_down(pygame.K_LEFT)) * m.meters_to_pixels(5) * dt
        m.y_offset_pixel += -(g.is_key_down(pygame.K_DOWN) -
                              g.is_key_down(pygame.K_UP)) * m.meters_to_pixels(5) * dt

        # Zoom control
        if g.is_key_pressed(pygame.K_KP_PLUS):
            m.set_pixels_per_meter(m.pixels_per_meter * 2)
        elif g.is_key_pressed(pygame.K_KP_MINUS):
            m.set_pixels_per_meter(m.pixels_per_meter // 2)


        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        self.mouse_rec = (mouse_pos_meter.x, mouse_pos_meter.y, 1.0, 1.0)

        print(self.t.check_collision_rec(self.mouse_rec))
        if g.is_key_down(pygame.K_b):
            # self.t.destroy_rectangle(self.mouse_rec)
            self.t.destroy_circle(mouse_pos_meter, 1)

        self.t.update()

        self.object_manager.update(dt)

    def draw(self):
        g.window.fill((25, 25, 25))
        self.t.draw()
        gr.draw_grid()
        gr.draw_rectangle(self.mouse_rec[0], self.mouse_rec[1], self.mouse_rec[2], self.mouse_rec[3], (255, 255, 0))
        self.object_manager.draw()

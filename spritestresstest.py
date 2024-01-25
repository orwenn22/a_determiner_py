from engine.state import state
from engine import graphics as gr, globals as g, metrics as m
import pygame


class SpriteStressTest(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit
        m.set_pixels_per_meter(50)

        # Put the cam at the center of the world
        m.set_camera_center(pygame.math.Vector2(0, 0))

        # This is the sprite for the stress test
        self.my_sprite = pygame.image.load("./testsprite.png")
        self.big_my_sprite = pygame.transform.scale(self.my_sprite, (1280 * 10, 720 * 10))
        self.rot = 0.0

    def update(self, dt: float):
        if g.is_key_pressed(pygame.K_t):
            import teststate
            self.manager.set_state(teststate.TestState())
            print(self)
            return

        # Move the camera at 5 meters / sec
        m.x_offset_pixel += -(g.is_key_down(pygame.K_RIGHT) -
                              g.is_key_down(pygame.K_LEFT)) * m.meters_to_pixels(5) * dt
        m.y_offset_pixel += -(g.is_key_down(pygame.K_DOWN) -
                              g.is_key_down(pygame.K_UP)) * m.meters_to_pixels(5) * dt

        self.rot += 4 * dt

    def draw(self):
        g.window.fill((25, 25, 25))
        gr.draw_grid()

        # Draw a HUUUGE sprite to see how much it reduces framerate
        gr.draw_sprite(self.big_my_sprite, pygame.Vector2(0, 0))

        # Uncomment stuff here to test features
        for i in range(0, 10000):
            gr.draw_sprite(self.my_sprite, pygame.Vector2(i, 0))
        #    gr.draw_sprite_scale(my_sprite, (i, 0, float(10), float(10)))
        #    gr.draw_sprite_rot(my_sprite, pygame.math.Vector2(i, 0), pygame.math.Vector2(2, 1), my_rot)

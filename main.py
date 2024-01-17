import pygame

import globals as g
import graphics as gr
from testobj import *

def main():
    pygame.init()
    window = g.init_window(1280, 720)
    default_font = pygame.font.SysFont(None, 24)

    print("wow")

    o = TestObj(1, 1)

    while g.handle_event():
        if g.is_key_pressed(pygame.K_DOWN):
            print("wow")

        # Update
        o.update()

        # Process physic
        o.process_physics(g.deltatime)

        # Draw
        g.window.fill((25, 25, 25))
        fps_text = default_font.render("FPS: " + str(g.get_fps()), True, (255, 255, 255))
        window.blit(fps_text, (10, 10))
        dt_text = default_font.render("DT: " + str(g.deltatime) + "s", True, (255, 0, 0))
        gr.draw_grid()

        window.blit(dt_text, (10, 34))
        o.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
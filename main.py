import pygame

import globals as g
from testobj import *

def main():
    pygame.init()
    window = g.init_window(1280, 720)
    default_font = pygame.font.SysFont(None, 24)

    print("wow")

    o = TestObj(60, 600)

    while g.handle_event():
        if g.is_key_pressed(pygame.K_DOWN):
            print("wow")

        # Update
        o.update()

        # Process physic
        o.process_physics(g.deltatime)

        # Draw
        #g.window.fill((25, 25, 25))

        fps_text = default_font.render("FPS: " + str(g.get_fps()), True, (255, 255, 255))
        window.blit(fps_text, (10, 10))

        o.draw()

        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
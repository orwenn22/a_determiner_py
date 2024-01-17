import pygame

import globals as g
import graphics as gr
import metrics as m
from testobj import *

def main():
    pygame.init()
    window = g.init_window(1280, 720)
    default_font = pygame.font.SysFont(None, 24)

    print("wow")

    o = TestObj(1, 1)
    #gr.pixels_per_meter = 25

    while g.handle_event():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)

        m.x_offset_pixel += -(g.is_key_down(pygame.K_RIGHT) - g.is_key_down(pygame.K_LEFT))
        m.y_offset_pixel += -(g.is_key_down(pygame.K_DOWN) - g.is_key_down(pygame.K_UP))

        # Update
        o.update()

        # Process physic (maybe do this in the object's update ? idk)
        o.process_physics(g.deltatime)

        # Draw
        g.window.fill((25, 25, 25))
        gr.draw_grid()
        o.draw()

        fps_text = default_font.render("FPS: " + str(g.get_fps()), True, (255, 255, 255))
        window.blit(fps_text, (10, 10))
        dt_text = default_font.render("DT: " + str(g.deltatime) + "s", True, (255, 0, 0))
        window.blit(dt_text, (10, 34))
        mouse_pos_text = default_font.render(f"Mouse : px : {mouse_x} {mouse_y} | m : {mouse_pos_meter.x} {mouse_pos_meter.y}", True, (255, 255, 255))
        window.blit(mouse_pos_text, (10, 58))


        pygame.display.flip()       # put this in handle event ???

    pygame.quit()


if __name__ == '__main__':
    main()
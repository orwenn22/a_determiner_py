from engine import metrics as m, graphics as gr, globals as g
import testobj
import pygame


def main():
    pygame.init()
    window = g.init_window(1280, 720)
    # it's illegal apparently the None TODO : redo it
    default_font = pygame.font.SysFont(None, 24)

    print("wow")

    o = testobj.TestObj(1, 1)
    o2 = testobj.TestObj(3, 1, 20)
    m.pixels_per_meter = 50


    my_sprite = pygame.image.load("./testsprite.png")
    my_rot = 0.0

    while g.handle_event():
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos_meter = m.window_position_to_meters_position(
            mouse_x, mouse_y)

        # Update
        my_rot += 4*g.deltatime

        # Move the camera at 5 meters / sec
        m.x_offset_pixel += -(testobj.g.is_key_down(pygame.K_RIGHT) -
                              testobj.g.is_key_down(pygame.K_LEFT)) * m.meters_to_pixels(5) * g.deltatime
        m.y_offset_pixel += -(testobj.g.is_key_down(pygame.K_DOWN) -
                              testobj.g.is_key_down(pygame.K_UP)) * m.meters_to_pixels(5) * g.deltatime
        o.update(g.deltatime)
        o2.update(g.deltatime)

        # Process physic (maybe do this in the object's update ? idk)
        o.process_physics(g.deltatime)
        o2.process_physics(g.deltatime)

        # Draw

        g.window.fill((25, 25, 25))
        gr.draw_grid()
        o.draw()
        o2.draw()

        for i in range(0, 10000):
            gr.draw_sprite(my_sprite, pygame.Vector2(i, 0))
            #gr.draw_sprite_scale(my_sprite, (i, 0, float(0.5), float(0.5)))
            #gr.draw_sprite_rot(my_sprite, pygame.math.Vector2(i, 0), pygame.math.Vector2(2, 1), my_rot)

        fps_text = default_font.render(
            "FPS: " + str(g.get_fps()), True, (255, 255, 255))
        window.blit(fps_text, (10, 10))
        dt_text = default_font.render(
            "DT: " + str(g.deltatime) + "s", True, (255, 0, 0))
        window.blit(dt_text, (10, 34))
        mouse_pos_text = default_font.render(
            f"Mouse : px : {mouse_x} {mouse_y} | m : {mouse_pos_meter.x} {mouse_pos_meter.y}", True, (255, 255, 255))
        window.blit(mouse_pos_text, (10, 58))

        pygame.display.flip()       # put this in handle event ???

    pygame.quit()


if __name__ == '__main__':
    main()

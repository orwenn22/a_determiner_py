from engine import metrics as m, globals as g
from engine.state import statemanager
import teststate
import pygame

# print(type(object_manager.list_object[0]))
# print(testobj.ko.entityobject.EntityObject.__subclasses__())  # Get all subclasses (don't include subclasses of subclasses or itself)
# print(testobj.ko.entityobject.EntityObject.__subclasscheck__(testobj.ko.entityobject.EntityObject))  # this check if it is a subclass of object (include subclasses of subclasses and itself)


def main():
    pygame.init()
    window = g.init_window(1280, 720,"game")
    
    default_font = pygame.font.SysFont(pygame.font.get_default_font(), 24)

    state_manager = statemanager.StateManager(teststate.TestState())

    while g.handle_event():
        # Getting the mouse position, for both absolute and world coordinates.
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        cam_center = m.get_camera_center()

        # Update
        state_manager.update(g.deltatime)

        # Draw
        state_manager.draw()

        # Some debug infos
        fps_text = default_font.render("FPS: " + str(g.get_fps()), True, (255, 255, 255))
        window.blit(fps_text, (10, 10))
        dt_text = default_font.render("DT: " + str(g.deltatime) + "s", True, (255, 0, 0))
        window.blit(dt_text, (10, 34))
        mouse_pos_text = default_font.render(
            f"Mouse : px : {mouse_x} {mouse_y} | m : {mouse_pos_meter.x} {mouse_pos_meter.y}",
            True, (255, 255, 255))
        window.blit(mouse_pos_text, (10, 58))
        cam_pos_text = default_font.render("Cam center: " + str(cam_center), True, (255, 255, 255))
        window.blit(cam_pos_text, (10, 80))

        g.game_loop_end()

    pygame.quit()


if __name__ == '__main__':
    main()

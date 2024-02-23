from engine import metrics as m, globals as g
from engine.state import statemanager
import globalresources as res
import pyray
from menus import menustate


def main():
    show_debug = False
    g.init_window(960, 540, "À déterminer™")
    res.init_resources()

    # state_manager = statemanager.StateManager(gameplaystate.GameplayState())
    state_manager = statemanager.StateManager(menustate.MenuState())
    while g.handle_event():
        # Getting the mouse position, for both absolute and world coordinates.
        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        cam_center = m.get_camera_center()

        if g.is_key_pressed(pyray.KeyboardKey.KEY_F3):
            show_debug = not show_debug

        # Update
        state_manager.update(g.deltatime)

        # Draw
        pyray.begin_drawing()
        state_manager.draw()

        # Some debug infos
        if show_debug:
            pyray.draw_fps(10, 10)
            pyray.draw_text("DT: " + str(g.deltatime) + "s", 10, 30, 20, pyray.Color(255, 0, 0, 255))
            pyray.draw_text(f"Mouse : px : {mouse_x} {mouse_y} | m : {mouse_pos_meter.x} {mouse_pos_meter.y}", 10, 50, 20, pyray.Color(
                255, 255, 255, 255))
            pyray.draw_text("Cam center: (" + str(cam_center.x) + ", " + str(cam_center.y) + ")",
                            10, 70, 20, pyray.Color(255, 255, 255, 255))
            pyray.draw_text(f"Current state : {type(state_manager.state).__name__} ({type(state_manager.state)})",
                            10, 90, 20, pyray.WHITE)

        pyray.end_drawing()
        g.game_loop_end()

    state_manager.unload()
    res.unload_resources()
    pyray.close_window()


if __name__ == '__main__':
    main()

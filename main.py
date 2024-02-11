from engine import metrics as m, globals as g
from engine.state import statemanager
import pyray
import teststate

# print(type(object_manager.list_object[0]))
# print(testobj.ko.entityobject.EntityObject.__subclasses__())  # Get all subclasses (don't include subclasses of subclasses or itself)
# print(testobj.ko.entityobject.EntityObject.__subclasscheck__(testobj.ko.entityobject.EntityObject))  # this check if it is a subclass of object (include subclasses of subclasses and itself)


def main():
    g.init_window(512, 512, "title")

    state_manager = statemanager.StateManager(teststate.TestState())

    while g.handle_event():
        # Getting the mouse position, for both absolute and world coordinates.
        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        cam_center = m.get_camera_center()

        # Update
        state_manager.update(g.deltatime)

        # Draw
        pyray.begin_drawing()
        state_manager.draw()

        # Some debug infos
        pyray.draw_fps(10, 10)
        pyray.draw_text("DT: " + str(g.deltatime) + "s", 10, 30, 20, pyray.Color(255, 0, 0, 255))
        pyray.draw_text(f"Mouse : px : {mouse_x} {mouse_y} | m : {mouse_pos_meter.x} {mouse_pos_meter.y}", 10, 50, 20, pyray.Color(255, 255, 255, 255))
        pyray.draw_text("Cam center: (" + str(cam_center.x) + ", " + str(cam_center.y) + ")", 10, 70, 20, pyray.Color(255, 255, 255, 255))

        pyray.end_drawing()
        g.game_loop_end()

    pyray.close_window()


if __name__ == '__main__':
    main()

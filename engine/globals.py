import pyray

print("globals module instantiated")

deltatime: float = 0.0      # This is in seconds
FPS: int = 120
zoom_changed: bool = False
mouse_wheel: int = 0
mouse_used: bool = False
running: bool = True


def init_window(w, h, game_name) -> None:
    global deltatime, running
    running = True  # just in case
    pyray.set_config_flags(pyray.ConfigFlags.FLAG_WINDOW_RESIZABLE)
    pyray.init_window(w, h, game_name)
    pyray.set_target_fps(240)
    deltatime = pyray.get_time()       # Perfect approximation for the first frame


def handle_event() -> bool:
    global keys_pressed, zoom_changed, mouse_wheel, mouse_used
    mouse_used = False
    r = not pyray.window_should_close() and running
    zoom_changed = False
    mouse_wheel = int(pyray.get_mouse_wheel_move())
    return r


def game_loop_end():
    global deltatime
    deltatime = pyray.get_frame_time()
#    deltatime = clock.tick(FPS) / 1000  # devide by 1000 to convert ms to s


def is_key_down(key) -> bool:
    return pyray.is_key_down(key)


def is_key_pressed(key) -> bool:
    return pyray.is_key_pressed(key)


def is_mouse_button_down(button) -> bool:
    return pyray.is_mouse_button_down(button)


def is_mouse_button_pressed(button) -> bool:
    return pyray.is_mouse_button_pressed(button)


def get_fps() -> float:
    return pyray.get_fps()

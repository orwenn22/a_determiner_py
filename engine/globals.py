import pyray

print("globals module instantiated")

running = False
keyboard_state = []
keys_pressed = {}
deltatime: float = 0.0      # This is in seconds
FPS: int = 120
zoom_changed: bool = False


def init_window(w, h, game_name) -> None:
    global running, deltatime
    running = True
    pyray.set_config_flags(pyray.ConfigFlags.FLAG_WINDOW_RESIZABLE)
    pyray.init_window(w, h, game_name)
    pyray.set_target_fps(240)
    deltatime = pyray.get_time()       # Perfect approximation for the first frame


# def update_keyboard_state():
#     global keyboard_state
#     #keyboard_state = pyray.get_key_pressed()

def handle_event() -> bool:
    global keys_pressed, running, zoom_changed
    keys_pressed.clear()
    zoom_changed = False
    if pyray.window_should_close():
        running = False
    key: int = pyray.get_key_pressed()
    if key != 0:
        keys_pressed[key] = True

    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         running = False
    #     elif event.type == pygame.KEYDOWN:
    #         keys_pressed[event.key] = True
        # TODO : handle key up events ?
#    update_keyboard_state()
    return running


def game_loop_end():
    global deltatime
    deltatime = pyray.get_time()
#    deltatime = clock.tick(FPS) / 1000  # devide by 1000 to convert ms to s
    # pygame.display.flip()

#
# def is_key_down(key) -> bool:
#     return keyboard_state[key]
#
#
# def is_key_pressed(key) -> bool:
#     if key not in keys_pressed:
#         return False
#     return keys_pressed[key]
#
#
#     return clock.get_fps()
# def get_fps() -> float:

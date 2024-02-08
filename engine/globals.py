import pygame

print("globals module instantiated")

running = False
window: pygame.Surface = None       # This is the surface of the main window
clock: pygame.time.Clock = None
keyboard_state = []
keys_pressed = {}
mouse_state = []
mouse_button_pressed = {}
deltatime: float = 0.0      # This is in seconds
FPS: int = 120
zoom_changed: bool = False


def init_window(w, h) -> pygame.Surface:
    global window, running, clock, deltatime
    running = True
    window = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    deltatime = 1/120 / 1000        # Perfect approximation for the first frame
    return window


def update_keyboard_state():
    global keyboard_state, mouse_state
    keyboard_state = pygame.key.get_pressed()
    mouse_state = pygame.mouse.get_pressed()


def handle_event() -> bool:
    global keys_pressed, running, zoom_changed
    keys_pressed.clear()
    mouse_button_pressed.clear()
    zoom_changed = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_button_pressed[event.button] = True
        # TODO : handle key up events ?
    update_keyboard_state()
    return running


def game_loop_end():
    global deltatime
    deltatime = clock.tick(FPS) / 1000  # devide by 1000 to convert ms to s
    pygame.display.flip()


def is_key_down(key) -> bool:
    return keyboard_state[key]


def is_key_pressed(key) -> bool:
    if key not in keys_pressed:
        return False
    return keys_pressed[key]


def is_mouse_button_down(button) -> bool:
    return mouse_state[button-1]


def is_mouse_button_pressed(button) -> bool:
    if button not in mouse_button_pressed:
        return False
    return mouse_button_pressed[button]

def get_fps() -> float:
    return clock.get_fps()

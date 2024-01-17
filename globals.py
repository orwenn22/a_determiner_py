import pygame

print("globals module instantiated")

running = False
window: pygame.Surface = None       # This is the surface of the main window
clock: pygame.time.Clock = None
keyboard_state = []
keys_pressed = {}
deltatime: float = 0.0      # This is in seconds
FPS: int = 120


def init_window(w, h) -> pygame.Surface:
    global window, running, clock, deltatime
    running = True
    window = pygame.display.set_mode((w, h), pygame.RESIZABLE)
    clock = pygame.time.Clock()
    deltatime = 1/120 / 1000        # Perfect aproximation for the first frame
    return window


def update_keyboard_state():
    global keyboard_state
    keyboard_state = pygame.key.get_pressed()



def handle_event() -> bool:
    global keys_pressed, running, deltatime
    deltatime = clock.tick(FPS)/1000     #devide by 1000 to convert ms to s
    keys_pressed.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
        # TODO : handle key up events ?
    update_keyboard_state()
    return running


def is_key_down(key) -> bool:
    return keyboard_state[key]


def is_key_pressed(key) -> bool:
    if key not in keys_pressed:
        return False
    return keys_pressed[key]

def get_fps() -> float:
    return clock.get_fps()

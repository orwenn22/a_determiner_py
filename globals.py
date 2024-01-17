import pygame

running = False
window : pygame.Surface = None
clock = None
keyboard_state = []
keys_pressed = {}
deltatime = 0.0
FPS = 120


def init_window(w, h):
    global window, running, clock
    running = True
    window = pygame.display.set_mode((w, h))
    clock = pygame.time.Clock()
    return window


def update_keyboard_state():
    global keyboard_state
    keyboard_state = pygame.key.get_pressed()



def handle_event():
    global keys_pressed, running, deltatime
    deltatime = clock.tick(FPS)/1000     #devide by 1000 to get it in sec
    keys_pressed.clear()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
    update_keyboard_state()
    return running


def is_key_down(key) -> bool:
    return keyboard_state[key]


def is_key_pressed(key):
    if key not in keys_pressed:
        return False
    return keys_pressed[key]

def get_fps():
    return clock.get_fps()

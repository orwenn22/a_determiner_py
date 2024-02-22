import pyray

portal_gun_sprite: pyray.Texture = None
menu_bg_sprite: pyray.Texture = None
menu_bg_option_sprite: pyray.Texture = None
menu_bg_credits_sprite: pyray.Texture = None
cool_transition_sprite: pyray.Texture = None
tiled_button_sprite: pyray.Texture = None
tiled_button_left_sprite: pyray.Texture = None
tiled_button_right_sprite: pyray.Texture = None
trowel_sprite: pyray.Texture = None
wall_sprite: pyray.Texture = None

def init_resources():
    global portal_gun_sprite, menu_bg_sprite, menu_bg_option_sprite, menu_bg_credits_sprite, cool_transition_sprite, \
           tiled_button_sprite, tiled_button_left_sprite, tiled_button_right_sprite, trowel_sprite

    portal_gun_sprite = pyray.load_texture("res/portal_gun.png")
    trowel_sprite = pyray.load_texture("res/trowel_sprite.png")
    menu_bg_sprite = pyray.load_texture("res/menubg.png")
    menu_bg_option_sprite = pyray.load_texture("res/menubg_option.png")
    menu_bg_credits_sprite = pyray.load_texture("res/menubg_credits_alt.png")
    cool_transition_sprite = pyray.load_texture("res/cool_transition.png")
    tiled_button_sprite = pyray.load_texture("res/tiled_button.png")
    tiled_button_left_sprite = pyray.load_texture("res/tiled_button_left.png")
    tiled_button_right_sprite = pyray.load_texture("res/tiled_button_right.png")

def unload_resources():
    pyray.unload_texture(tiled_button_right_sprite)
    pyray.unload_texture(tiled_button_left_sprite)
    pyray.unload_texture(tiled_button_sprite)
    pyray.unload_texture(cool_transition_sprite)
    pyray.unload_texture(menu_bg_credits_sprite)
    pyray.unload_texture(menu_bg_option_sprite)
    pyray.unload_texture(menu_bg_sprite)
    pyray.unload_texture(portal_gun_sprite)
    pyray.unload_texture(trowel_sprite)
    pyray.unload_texture(wall_sprite)

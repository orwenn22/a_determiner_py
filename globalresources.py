import pyray

portal_gun_sprite: pyray.Texture = None
menu_bg_sprite: pyray.Texture = None
menu_bg_option_sprite: pyray.Texture = None
menu_bg_credits_sprite: pyray.Texture = None

def init_resources():
    global portal_gun_sprite, menu_bg_sprite, menu_bg_option_sprite, menu_bg_credits_sprite
    portal_gun_sprite = pyray.load_texture("res/portal_gun.png")
    menu_bg_sprite = pyray.load_texture("res/menubg.png")
    menu_bg_option_sprite = pyray.load_texture("res/menubg_option.png")
    menu_bg_credits_sprite = pyray.load_texture("res/menubg_credits.png")

def unload_resources():
    pyray.unload_texture(menu_bg_credits_sprite)
    pyray.unload_texture(menu_bg_option_sprite)
    pyray.unload_texture(menu_bg_sprite)
    pyray.unload_texture(portal_gun_sprite)

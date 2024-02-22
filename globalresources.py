import pyray

portal_gun_sprite: pyray.Texture = None

def init_resources():
    global portal_gun_sprite
    portal_gun_sprite = pyray.load_texture("portal_gun.png")

def unload_resources():
    pyray.unload_texture(portal_gun_sprite)

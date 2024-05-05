import pyray

portal_gun_sprite: pyray.Texture = None
portal_remover_sprite: pyray.Texture = None
menu_bg_sprite: pyray.Texture = None
menu_bg_option_sprite: pyray.Texture = None
menu_bg_credits_sprite: pyray.Texture = None
menu_bg_grayscale_sprite: pyray.Texture = None
cool_transition_sprite: pyray.Texture = None
tiled_button_sprite: pyray.Texture = None
tiled_button_left_sprite: pyray.Texture = None
tiled_button_right_sprite: pyray.Texture = None
trowel_sprite: pyray.Texture = None
wall_sprite: pyray.Texture = None
default_void_sprite: pyray.Texture = None
portal_sprite: pyray.Texture = None
explosion_spritesheet: pyray.Texture = None
mini_ded_sprite: pyray.Texture = None
mini_blue_sprite: pyray.Texture = None
mini_red_sprite: pyray.Texture = None
green_marker_sprite: pyray.Texture = None
shoot_action_sprite: pyray.Texture = None
jump_action_sprite: pyray.Texture = None
spdiamond_sprite: pyray.Texture = None
player_jump_sprite: pyray.Texture = None
player_injump_sprite: pyray.Texture = None
player_sprite: pyray.Texture = None
player_shooting_sprite: pyray.Texture = None
player_portal_sprite: pyray.Texture = None
player_wall_sprite: pyray.Texture = None
strength_upgrade_sprite: pyray.Texture = None
strength_downgrade_sprite: pyray.Texture = None
potato_sprite: pyray.Texture = None


def init_resources():
    global portal_gun_sprite, menu_bg_sprite, menu_bg_option_sprite, menu_bg_credits_sprite, cool_transition_sprite, \
           tiled_button_sprite, tiled_button_left_sprite, tiled_button_right_sprite, trowel_sprite, wall_sprite, \
           explosion_spritesheet, default_void_sprite, portal_sprite, mini_blue_sprite, mini_red_sprite, \
           mini_ded_sprite, green_marker_sprite, menu_bg_grayscale_sprite, shoot_action_sprite, jump_action_sprite, \
           spdiamond_sprite, player_jump_sprite, player_injump_sprite, player_sprite, player_shooting_sprite, \
           player_portal_sprite, player_wall_sprite, portal_remover_sprite, strength_upgrade_sprite, \
           strength_downgrade_sprite, potato_sprite

    wall_sprite = pyray.load_texture("res/wall.png")
    portal_gun_sprite = pyray.load_texture("res/portal_gun.png")
    portal_remover_sprite = pyray.load_texture("res/portal_remover.png")
    trowel_sprite = pyray.load_texture("res/truelle.png")
    menu_bg_sprite = pyray.load_texture("res/menubg.png")
    menu_bg_option_sprite = pyray.load_texture("res/menubg_option.png")
    menu_bg_credits_sprite = pyray.load_texture("res/menubg_credits_alt.png")
    menu_bg_grayscale_sprite = pyray.load_texture("res/menubg_grayscale.png")
    cool_transition_sprite = pyray.load_texture("res/cool_transition.png")
    tiled_button_sprite = pyray.load_texture("res/tiled_button.png")
    tiled_button_left_sprite = pyray.load_texture("res/tiled_button_left.png")
    tiled_button_right_sprite = pyray.load_texture("res/tiled_button_right.png")
    explosion_spritesheet = pyray.load_texture("res/explosion-boom.png")
    default_void_sprite = pyray.load_texture("res/default.png")
    portal_sprite = pyray.load_texture("res/portal.png")
    mini_ded_sprite = pyray.load_texture("res/mini_ded.png")
    mini_blue_sprite = pyray.load_texture("res/mini_blue.png")
    mini_red_sprite = pyray.load_texture("res/mini_red.png")
    green_marker_sprite = pyray.load_texture("res/green_marker.png")
    shoot_action_sprite = pyray.load_texture("res/cannon_sprite.png")
    jump_action_sprite = pyray.load_texture("res/jumping_sprite.png")
    spdiamond_sprite = pyray.load_texture("res/spdiamond_sprite.png")
    player_jump_sprite = pyray.load_texture("res/player_jump.png")
    player_injump_sprite = pyray.load_texture("res/player_injump.png")
    player_sprite = pyray.load_texture("res/player.png")
    player_shooting_sprite = pyray.load_texture("res/player_shooting.png")
    player_portal_sprite = pyray.load_texture("res/player_portal.png")
    player_wall_sprite = pyray.load_texture("res/player_wall.png")
    strength_upgrade_sprite = pyray.load_texture("res/strength_upgrade.png")
    strength_downgrade_sprite = pyray.load_texture("res/strength_downgrade.png")
    potato_sprite = pyray.load_texture("res/potato.png")


def unload_resources():
    pyray.unload_texture(potato_sprite)
    pyray.unload_texture(strength_downgrade_sprite)
    pyray.unload_texture(strength_upgrade_sprite)
    pyray.unload_texture(player_wall_sprite)
    pyray.unload_texture(player_portal_sprite)
    pyray.unload_texture(player_shooting_sprite)
    pyray.unload_texture(player_sprite)
    pyray.unload_texture(player_injump_sprite)
    pyray.unload_texture(player_jump_sprite)
    pyray.unload_texture(spdiamond_sprite)
    pyray.unload_texture(jump_action_sprite)
    pyray.unload_texture(shoot_action_sprite)
    pyray.unload_texture(green_marker_sprite)
    pyray.unload_texture(mini_red_sprite)
    pyray.unload_texture(mini_blue_sprite)
    pyray.unload_texture(mini_ded_sprite)
    pyray.unload_texture(portal_sprite)
    pyray.unload_texture(default_void_sprite)
    pyray.unload_texture(explosion_spritesheet)
    pyray.unload_texture(tiled_button_right_sprite)
    pyray.unload_texture(tiled_button_left_sprite)
    pyray.unload_texture(tiled_button_sprite)
    pyray.unload_texture(cool_transition_sprite)
    pyray.unload_texture(menu_bg_grayscale_sprite)
    pyray.unload_texture(menu_bg_credits_sprite)
    pyray.unload_texture(menu_bg_option_sprite)
    pyray.unload_texture(menu_bg_sprite)
    pyray.unload_texture(trowel_sprite)
    pyray.unload_texture(portal_remover_sprite)
    pyray.unload_texture(portal_gun_sprite)
    pyray.unload_texture(wall_sprite)

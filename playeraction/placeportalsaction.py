from . import playeraction

from engine import metrics as m, graphics as gr, globals as g
from gameobject import player, portal
import pyray
import globalresources as res


class PlacePortalsAction(playeraction.PlayerAction):
    def __init__(self):
        super().__init__()
        self.icon = res.portal_gun_sprite
        self.action_name = "Portal"
        self.first_portal = None
        self.is_item = True

        # For the character animation
        self.animation_time = 0             # Time since the beginning of the animation cycle (in seconds)
        self.animation_current_frame = 0    # Current frame being displayed
        self.animation_frame_count = 3      # Number of frames in the animation
        self.animation_duration = 1         # The time it take in second to loop through all the frames

    def on_update(self, _player: player.Player, dt: float):
        # Update character animation
        self.animation_time += dt
        self.animation_time %= self.animation_duration
        self.animation_current_frame = int((self.animation_time/self.animation_duration) * self.animation_frame_count)

        if g.mouse_used: return
        if not g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT): return

        print("Placing portal")

        # If we get here it means we need to place the portal
        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
        mouse_meters = m.window_position_to_meters_position(mouse_x, mouse_y)

        p = portal.Portal(mouse_meters.x, mouse_meters.y)
        if len(_player.manager.get_collision(p)) == 0 and not _player.parent_state.t.check_collision_rec(p.get_rectangle(), True):
            _player.manager.add_object(p)
            if self.first_portal is None:
                self.first_portal = p
                _player.parent_state.hide_action_widgets()
            else:
                p.set_destination(self.first_portal)
                self.first_portal.set_destination(p)
                _player.remove_action(self)
                _player.parent_state.show_action_widgets()
                _player.parent_state.stats["portal"][_player.team] += 1

        g.mouse_used = True

    def on_draw(self, _player: player.Player):
        _player.block_default_sprite = True
        gr.draw_sprite_rot_ex(res.player_portal_sprite,
                              pyray.Rectangle(self.animation_current_frame*32, _player.team * 47, 32, 47),      # Sprite is 32*47
                              pyray.Vector2(_player.position.x, _player.position.y - 0.46875 / 2),      # The last part is to make sure the portal part is right above the hitbox
                              pyray.Vector2(1, 1.46875),  # 47/32 = 1,46875
                              0)

        # If the mouse is on a UI element then we don't draw the portal preview
        if g.mouse_used: return

        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
        mouse_meters = m.window_position_to_meters_position(mouse_x, mouse_y)
        gr.draw_circle(mouse_meters, 0.5, (150, 92, 191, 127))

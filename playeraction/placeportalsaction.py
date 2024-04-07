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

    def on_update(self, _player: player.Player, dt: float):
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
        if g.mouse_used: return

        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
        mouse_meters = m.window_position_to_meters_position(mouse_x, mouse_y)
        gr.draw_circle(mouse_meters, 0.5, (150, 92, 191, 127))

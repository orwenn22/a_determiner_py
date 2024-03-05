from . import playeraction
from objects import wall, player
from engine import globals as g
import key
from engine import graphics as gr
from engine.object import kinematicprediction
import math
import globalresources as res


class PlaceWallAction(playeraction.PlayerAction):
    def __init__(self):
        super().__init__()
        self.action_name = "Wall\n(item)"
        self.wall_height = 1        # Put this to 2 ?
        
    def on_click(self, _player: player.Player, action_index: int):
        super().on_click(_player, action_index)
        _player.throw_angle = 0

    def on_update(self, _player: player.Player, dt: float):
        if g.is_key_pressed(key.key_binds["right"]):
            _player.throw_angle = 0
        elif g.is_key_pressed(key.key_binds["left"]):
            _player.throw_angle = math.pi

        if g.is_key_pressed(key.key_binds["action"]):
            wall_height = self.wall_height
            w = wall.Wall(_player.position.x + math.cos(_player.throw_angle) * 2, _player.position.y, 0.5, wall_height, _player.parent_state)

            # If the wall is clipping with the terrain then make it go up
            total_vertical_offset = 0
            while _player.parent_state.t.check_collision_rec(w.get_rectangle()):
                w.position.y -= 0.1
                total_vertical_offset += 0.1
                # Cancel, because in this case it would be wierd to spawn the wall too high
                if total_vertical_offset >= wall_height:
                    return

            # If the wall is clipping with another object then we don't spawn it
            if len(_player.manager.get_collision(w)) > 0:
                return

            _player.manager.add_object(w)
            _player.remove_action(self)
            _player.current_action = -1
            _player.parent_state.show_action_widgets()
            _player.throw_angle = 0

    def on_draw(self, _player: player.Player):
        w = wall.Wall(_player.position.x + math.cos(_player.throw_angle) * 2,
                      _player.position.y, 0.5, self.wall_height,
                      _player.parent_state)

        wall_prediction = kinematicprediction.KinematicPrediction.from_other_object(w)
        wall_prediction.draw_simulation(10, c=(255, 100, 100, 255))
        gr.draw_sprite_scale(res.wall_sprite, w.get_rectangle(), (255, 255, 255, 127))

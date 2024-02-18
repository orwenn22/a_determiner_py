import pyray, math

from . import playeraction
import player, gameplaystate
from engine import globals as g
from engine.object import kinematicprediction


class JumpAction(playeraction.PlayerAction):
    def __init__(self):
        super().__init__()
        self.action_name = "Jump"

    def on_update(self, _player: player.Player, dt: float):
        _player.throw_angle += (g.is_key_down(pyray.KeyboardKey.KEY_D) - g.is_key_down(pyray.KeyboardKey.KEY_Q)) * dt
        if g.is_key_pressed(pyray.KeyboardKey.KEY_SPACE) and _player.action_points >= 20:
            _player.action_points -= 20
            _player.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / dt,
                                              math.sin(_player.throw_angle) * _player.strength / dt))
            _player.enable_physics = True
            _player.use_small_hitbox = True
            _player.current_action = -1
            _player.parent_state.actions_widgets.clear()

    def on_draw(self, _player: player.Player):
        # 0.01 is the default dt for kinematic predictions
        a = kinematicprediction.KinematicPrediction.from_other_object(_player)
        a.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / 0.01,
                                    math.sin(_player.throw_angle) * _player.strength / 0.01))
        a.draw_simulation(10)

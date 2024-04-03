import pyray
import math

import key
from . import playeraction
from gameobject import player
from engine import globals as g
from engine.object import kinematicprediction
import globalresources as res


class JumpAction(playeraction.PlayerAction):
    def __init__(self):
        super().__init__()
        self.action_cost = 20
        self.action_name = "Jump"
        self.icon = res.jump_action_sprite

    def on_update(self, _player: player.Player, dt: float):
        _player.throw_angle += (g.is_key_down(key.key_binds["right"]) - g.is_key_down(key.key_binds["left"])) * dt
        if g.is_key_pressed(key.key_binds["action"]) and _player.action_points >= self.action_cost:
            _player.action_points -= self.action_cost
            _player.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / dt,
                                              math.sin(_player.throw_angle) * _player.strength / dt))
            _player.enable_physics = True
            _player.use_small_hitbox = True
            _player.current_action = -1
            _player.parent_state.hide_action_widgets()
            _player.parent_state.stats["jump"][_player.team] += 1

    def on_draw(self, _player: player.Player):
        # 0.01 is the default dt for kinematic predictions
        a = kinematicprediction.KinematicPrediction.from_other_object(_player)
        a.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / 0.01,
                                    math.sin(_player.throw_angle) * _player.strength / 0.01))
        a.draw_simulation(10)

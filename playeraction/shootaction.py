import pyray
import math

import key
from . import playeraction      # TODO : fix this
from engine import globals as g
from engine.object import kinematicprediction
from gameobject import bullet, player


class ShootAction(playeraction.PlayerAction):

    def __init__(self):
        super().__init__()
        self.action_cost = 25
        self.action_name = f"Shoot\n(-{str(self.action_cost)})"

    def on_update(self, _player: player.Player, dt: float):
        _player.throw_angle += (g.is_key_down(key.key_binds["right"]) - g.is_key_down(key.key_binds["left"])) * dt
        if g.is_key_pressed(key.key_binds["action"]) and _player.action_points >= self.action_cost:
            b = bullet.Bullet(_player.position.x, _player.position.y, _player.parent_state, _player, True)
            b.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / dt,
                                        math.sin(_player.throw_angle) * _player.strength / dt))
            _player.manager.add_object(b)
            _player.action_points -= self.action_cost
            _player.parent_state.stats["blue_shoot" if _player.team==0 else "red_shoot"] += 1

    def on_draw(self, _player: player.Player):
        b = bullet.Bullet(_player.position.x, _player.position.y, _player.parent_state, _player, True)
        a = kinematicprediction.KinematicPrediction.from_other_object(b)
        a.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / 0.01,
                                    math.sin(_player.throw_angle) * _player.strength / 0.01))
        a.draw_simulation(10)

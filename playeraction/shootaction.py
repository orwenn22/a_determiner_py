import pyray
import math

import key
from . import playeraction
from engine import globals as g, graphics as gr
from engine.object import kinematicprediction
from gameobject import bullet, player
import globalresources as res


class ShootAction(playeraction.PlayerAction):

    def __init__(self):
        super().__init__()
        self.action_cost = 25
        self.action_name = "Shoot"
        self.icon = res.shoot_action_sprite

    def on_update(self, _player: player.Player, dt: float):
        _player.throw_angle += (g.is_key_down(key.key_binds["right"]) - g.is_key_down(key.key_binds["left"])) * dt
        if g.is_key_pressed(key.key_binds["action"]) and _player.action_points >= self.action_cost:
            b = bullet.Bullet(_player.position.x, _player.position.y, _player.parent_state, _player, True)
            b.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / dt,
                                        math.sin(_player.throw_angle) * _player.strength / dt))
            _player.manager.add_object(b)
            _player.action_points -= self.action_cost
            _player.parent_state.stats["shoot"][_player.team] += 1

    def on_draw(self, _player: player.Player):
        b = bullet.Bullet(_player.position.x, _player.position.y, _player.parent_state, _player, True)
        a = kinematicprediction.KinematicPrediction.from_other_object(b)
        a.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / 0.01,
                                    math.sin(_player.throw_angle) * _player.strength / 0.01))
        a.draw_simulation(10)

        _player.block_default_sprite = True
        shooting_sprite = res.player_shooting_blue_sprite if _player.team == 0 else res.player_shooting_red_sprite
        gr.draw_sprite_rot_ex(shooting_sprite,
                              pyray.Rectangle(0, 0, shooting_sprite.width, shooting_sprite.height),
                              _player.position,
                              pyray.Vector2(1.0, 1.0),
                              0.0)

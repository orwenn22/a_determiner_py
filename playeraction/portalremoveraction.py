import math
import pyray

from . import playeraction
from engine import globals as g, graphics as gr
from engine.object import kinematicprediction
import globalresources as res
import key as key
from gameobject import player, portalremoverbullet


class PortalRemoverAction(playeraction.PlayerAction):
    def __init__(self):
        super().__init__()
        self.action_name = "Remover"
        self.is_item = True
        self.icon = res.portal_remover_sprite

    def on_update(self, _player: player.Player, dt: float):
        _player.throw_angle += (g.is_key_down(key.key_binds["right"]) - g.is_key_down(key.key_binds["left"])) * dt
        if g.is_key_pressed(key.key_binds["action"]) and _player.action_points >= self.action_cost:
            # Spawn the bullet
            b = portalremoverbullet.PortalRemoverBullet(_player.position.x, _player.position.y, _player.parent_state)
            b.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / dt,
                                        math.sin(_player.throw_angle) * _player.strength / dt))
            _player.manager.add_object(b)

            # Remove the item from the player
            _player.action_points -= self.action_cost
            # TODO : portal remover stat ?
            _player.remove_action(self)

    def on_draw(self, _player: player.Player):
        # Create a prediction with the bullet
        b = portalremoverbullet.PortalRemoverBullet(_player.position.x, _player.position.y, _player.parent_state)
        a = kinematicprediction.KinematicPrediction.from_other_object(b)
        a.apply_force(pyray.Vector2(math.cos(_player.throw_angle) * _player.strength / 0.01,
                                    math.sin(_player.throw_angle) * _player.strength / 0.01))       #0.01 is the default dt for kinematic prediction

        # Draw the result of the prediction
        a.draw_simulation(10, c=pyray.Color(200, 10, 10, 100))

        # Shooting sprite (maybe we need to replace it with something else ?)
        _player.block_default_sprite = True
        gr.draw_sprite_rot_ex(res.player_shooting_sprite,
                              pyray.Rectangle(0, _player.team * 32, 32, 32),  # Sprite is 32*32
                              _player.position,
                              pyray.Vector2(1.0, 1.0),
                              0.0)

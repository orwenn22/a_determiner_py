import pyray, math

from . import playeraction      # TODO : fix this
from engine import globals as g
from engine.object import kinematicprediction
import bullet


class ShootAction(playeraction.PlayerAction):
    import testobj

    def __init__(self):
        super().__init__()
        self.action_name = "Shoot"

    def on_update(self, player: testobj.TestObj, dt: float):
        player.throw_angle += (g.is_key_down(pyray.KeyboardKey.KEY_D) - g.is_key_down(pyray.KeyboardKey.KEY_Q)) * dt
        if g.is_key_pressed(pyray.KeyboardKey.KEY_SPACE) and player.action_points >= 25:
            b = bullet.Bullet(player.position.x, player.position.y, player.parent_state, player, True)
            b.apply_force(pyray.Vector2(math.cos(player.throw_angle) * player.strength / dt,
                                        math.sin(player.throw_angle) * player.strength / dt))
            player.manager.add_object(b)
            player.action_points -= 25

    def on_draw(self, player: testobj.TestObj):
        b = bullet.Bullet(player.position.x, player.position.y, player.parent_state, player, True)
        a = kinematicprediction.KinematicPrediction.from_other_object(b)
        a.apply_force(pyray.Vector2(math.cos(player.throw_angle) * player.strength / 0.01,
                                    math.sin(player.throw_angle) * player.strength / 0.01))
        a.draw_simulation(10)

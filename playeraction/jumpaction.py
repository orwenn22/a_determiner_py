import pyray, math

from . import playeraction
import testobj, gameplaystate
from engine import globals as g
from engine.object import kinematicprediction


class JumpAction(playeraction.PlayerAction):
    def __init__(self):
        super().__init__()
        self.action_name = "Jump"

    def on_update(self, player: testobj.TestObj, dt: float):
        player.throw_angle += (g.is_key_down(pyray.KeyboardKey.KEY_D) - g.is_key_down(pyray.KeyboardKey.KEY_Q)) * dt
        if g.is_key_pressed(pyray.KeyboardKey.KEY_SPACE) and player.action_points >= 20:
            player.action_points -= 20
            player.apply_force(pyray.Vector2(math.cos(player.throw_angle) * player.strength / dt,
                                             math.sin(player.throw_angle) * player.strength / dt))
            player.enable_physics = True
            player.use_small_hitbox = True
            player.current_action = -1
            player.parent_state.actions_widgets.clear()

    def on_draw(self, player: testobj.TestObj):
        # 0.01 is the default dt for kinematic predictions
        a = kinematicprediction.KinematicPrediction.from_other_object(player)
        a.apply_force(pyray.Vector2(math.cos(player.throw_angle) * player.strength / 0.01,
                                    math.sin(player.throw_angle) * player.strength / 0.01))
        a.draw_simulation(10)

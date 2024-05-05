from gameobject import player, explosion
from . import playeraction
import globalresources as res


class HotPotatoAction(playeraction.PlayerAction):
    def __init__(self):
        super().__init__()
        self.action_name = "Hot potato"
        self.is_item = True
        self.icon = res.potato_sprite

    def on_click(self, _player: player.Player, action_index: int):
        cols: list[player.Player] = _player.manager.get_collision(_player, player.Player)
        for p in cols:
            if p.team == _player.team:
                continue
            p.add_action(HotPotatoAction())
            _player.action_points += 10
            _player.remove_action(self)
            break

    def on_skip(self, _player: player.Player):
        _player.manager.add_object(explosion.Explosion(_player.position.x, _player.position.y, 2.5, _player.parent_state))
        _player.parent_state.kill_player(_player)
        return True     # Do this because killing the player will already skip the turn

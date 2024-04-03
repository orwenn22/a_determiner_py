import pyray

import engine.globals as g
import engine.metrics as m
import engine.widget.widget as widget
import globalresources as res
import playeraction.placeportalsaction as placeportalaction
import playeraction.spawnwall as spawnwall


class PlayersIndicator(widget.Widget):
    def __init__(self, gameplay_state):
        import gameplaystate
        self.scale = 2
        super().__init__(0, 5, 2, 16*self.scale, "TC")
        self.gameplay_state: gameplaystate.GameplayState = gameplay_state

        self.team_textures = [
            res.mini_blue_sprite,
            res.mini_red_sprite
        ]

    def update(self):
        player_count = len(self.gameplay_state.players)
        #                                   marge
        self.set_width((player_count*16 + (player_count-1)*2)*self.scale)

        if g.mouse_used or not self.is_hovered():
            return

        rel_mouse_x = int(pyray.get_mouse_x() - self.coordinate.x)
        player_index = rel_mouse_x // (18*self.scale)
        if g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            player = self.gameplay_state.players[player_index]
            if player is not None:
                m.set_camera_center(player.position)

        g.mouse_used = True

    def draw(self):
        painter_x = int(self.coordinate.x)
        for i in range(len(self.gameplay_state.players)):
            p = self.gameplay_state.players[i]
            painter_y = int(self.coordinate.y)
            if p is None:
                pyray.draw_texture_pro(res.mini_ded_sprite, pyray.Rectangle(0, 0, 16, 16),
                                       pyray.Rectangle(painter_x, painter_y, 16*self.scale, 16*self.scale),
                                       pyray.Vector2(0, 0), 0.0,
                                       pyray.WHITE)
                painter_x += 18*self.scale
                continue

            # Player icon
            texture = self.team_textures[p.team]
            pyray.draw_texture_pro(texture, pyray.Rectangle(0, 0, 16, 16),
                                   pyray.Rectangle(painter_x, painter_y, 16*self.scale, 16*self.scale),
                                   pyray.Vector2(0, 0), 0.0,
                                   pyray.WHITE)
            painter_y += 18*self.scale

            # Items
            for act in p.actions:
                texture = act.icon
                if texture is None or (not act.is_item):
                    continue
                pyray.draw_texture_pro(texture, pyray.Rectangle(0, 0, texture.width, texture.height),
                                       pyray.Rectangle(painter_x, painter_y, 16*self.scale, 16*self.scale),
                                       pyray.Vector2(0, 0), 0.0,
                                       pyray.WHITE)
                painter_y += 18*self.scale

            # Green marker
            if i == self.gameplay_state.current_player:
                pyray.draw_texture_pro(res.green_marker_sprite, pyray.Rectangle(0, 0, res.green_marker_sprite.width, -res.green_marker_sprite.height),
                                       pyray.Rectangle(painter_x, painter_y, 16*self.scale, 16*self.scale),
                                       pyray.Vector2(0, 0), 0.0,
                                       pyray.WHITE)
                painter_y += 18*self.scale

            painter_x += 18*self.scale

import pyray

import engine.widget.widget as widget
import globalresources as res
import playeraction.placeportalsaction as placeportalaction
import playeraction.spawnwall as spawnwall


class PlayersIndicator(widget.Widget):
    def __init__(self, gameplay_state):
        import gameplaystate

        super().__init__(0, 5, 2, 16, "TC")
        self.gameplay_state: gameplaystate.GameplayState = gameplay_state

        self.team_textures = [
            res.mini_blue_sprite,
            res.mini_red_sprite
        ]

        self.scale = 2

    def update(self):
        player_count = len(self.gameplay_state.players)
        #                                   marge
        self.set_width((player_count*16 + (player_count-1)*2)*self.scale)

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
                # TODO : better system for these icons ? Store textures in the actions themselves ?
                match type(act):
                    case placeportalaction.PlacePortalsAction:
                        texture = res.portal_gun_sprite
                    case spawnwall.PlaceWallAction:
                        texture = res.trowel_sprite
                    case _:
                        texture = None

                if texture is None:
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

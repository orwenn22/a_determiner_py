import pyray

from engine.widget import tiledbutton
import globalresources as res


class ActionButton(tiledbutton.TiledButton):
    def __init__(self, current_player, action_index: int):
        """
        This is a button that will select an action of the corresponding player when clicked.
        It is created from the player's get_action_widgets.
        :param current_player: the player linked to the action
        :param action_index: the index of the action in the player
        """
        from gameobject import player
        self.player: player.Player = current_player
        self.action_index = action_index
        button_size = 80

        # Create the callback
        def on_click():
            self.player.actions[self.action_index].on_click(self.player, self.action_index)

        # We don't need to set the positions of the widgets here because they
        # are calculated in GameplayState.show_action_widgets()
        super().__init__(0, 0, button_size, button_size, "BC",
                         res.tiled_button_sprite, 8, 2,
                         self.player.actions[self.action_index].action_name, on_click)

        self.set_font_color(pyray.WHITE)
        self.set_hovering_color(pyray.YELLOW)
        self.set_text_offset(8, 8)

    def update(self):
        self.set_color(pyray.RED if (self.player.current_action == self.action_index) else pyray.WHITE, False)
        super().update()

    def draw(self):
        super().draw()

        position_x = self.coordinate.x + self.hover_offset_x * self.hovered
        position_y = self.coordinate.y + self.hover_offset_y * self.hovered

        # Action const
        action_cost = self.player.actions[self.action_index].action_cost
        price_font_size = 10
        action_cost_text = "(item)" if (action_cost == 0) else f"(-{action_cost})"
        pyray.draw_text(action_cost_text,
                        int(position_x+8), int(position_y+self.height-8-price_font_size),
                        price_font_size, pyray.GRAY)

        # Action icon
        action_texture: pyray.Texture | None = self.player.actions[self.action_index].icon
        texture_width = 32
        texture_height = 32
        if action_texture is not None:
            pyray.draw_texture_pro(action_texture,
                                   pyray.Rectangle(0, 0, action_texture.width, action_texture.height),
                                   pyray.Rectangle(int(position_x + (self.width - texture_width)//2), int(position_y + (self.height - texture_height)//2), texture_width, texture_height),
                                   pyray.Vector2(0, 0), 0,
                                   pyray.WHITE)

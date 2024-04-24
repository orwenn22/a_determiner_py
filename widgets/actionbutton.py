import pyray

import widgets.fakeactionbutton as fakeactionbutton


class ActionButton(fakeactionbutton.FakeActionButton):
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

        is_item = self.player.actions[self.action_index].is_item
        action_cost = self.player.actions[self.action_index].action_cost

        # Create the callback
        def on_click():
            self.player.actions[self.action_index].on_click(self.player, self.action_index)

        super().__init__(self.player.actions[self.action_index].action_name,
                         "(item)" if is_item else f"(-{action_cost})",
                         on_click)

    def update(self):
        self.set_color(pyray.RED if (self.player.current_action == self.action_index) else pyray.WHITE, False)

        # Update price every frame in case price change is a thing in the future
        is_item = self.player.actions[self.action_index].is_item
        action_cost = self.player.actions[self.action_index].action_cost
        self.price_label = "(item)" if is_item else f"(-{action_cost})"

        super().update()

    def draw(self):
        super().draw()

        position_x = self.absolute_position.x + self.hover_offset_x * self.hovered
        position_y = self.absolute_position.y + self.hover_offset_y * self.hovered

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

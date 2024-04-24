import pyray

from engine.widget import tiledbutton
import globalresources as res


class FakeActionButton(tiledbutton.TiledButton):
    """
    This mostly exist for the skip button
    """
    def __init__(self, label: str, price_label: str, action):
        button_size = 80
        self.price_label = price_label

        # We don't need to set the positions of the widgets here because they
        # are calculated in GameplayState.show_action_widgets()
        # TODO : make it usable elsewhere if necessary ?
        super().__init__(0, 0, button_size, button_size, "BC",
                         res.tiled_button_sprite, 8, 2,
                         label, action)

        self.set_font_color(pyray.WHITE)
        self.set_hovering_color(pyray.YELLOW)
        self.set_text_offset(8, 8)

    def draw(self):
        super().draw()

        position_x = self.absolute_position.x + self.hover_offset_x * self.hovered
        position_y = self.absolute_position.y + self.hover_offset_y * self.hovered

        # Action cost

        price_font_size = 10
        pyray.draw_text(self.price_label,
                        int(position_x + 8), int(position_y + self.height - 8 - price_font_size),
                        price_font_size, pyray.GRAY)

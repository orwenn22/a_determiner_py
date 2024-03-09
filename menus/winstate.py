import pyray
from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton
import globalresources as res


class WinState(state.State):
    def __init__(self,winning_team:int, stats: dict, winners_left: int):
        from menus import menustate
        super().__init__()

        def back_to_main_menu():
            self.manager.set_state(menustate.MenuState())

        self.widget_manager = widgetmanager.WidgetManager()
        
        return_menu = tiledbutton.TiledButton(0, 70, 250, 70, "BC", res.tiled_button_sprite, 8, 2, label="Return to main menu", act=back_to_main_menu)
        return_menu.set_font_color(pyray.WHITE).set_scrollable(False).center_text().set_hovering_color(pyray.YELLOW)

        winner_str = "Victory of blue team" if winning_team == 0 else "Victory of red team"
        winner_text = label.Label(0, 50, "TC", winner_str, 28, pyray.BLACK)

        stats_window = tiledbutton.TiledButton(0, 0, 600, 400, "MC", res.tiled_button_sprite,8,2, label="Statistics")
        stats_window.set_text_offset(300 - pyray.measure_text(winner_str, stats_window.fontsize) // 2, 20).set_font_color(pyray.WHITE)
        stats_window.hover_offset_x = 0
        stats_window.hover_offset_y = 0

        self.widget_manager.add_widget(return_menu)
        self.widget_manager.add_widget(winner_text)
        self.widget_manager.add_widget(stats_window)
        
        self.bg_rect = pyray.Rectangle(0, 0, res.menu_bg_sprite.width, res.menu_bg_sprite.height)
        print(stats)

    def update(self, dt):
        self.bg_rect.x += 12*dt
        self.bg_rect.y += 12*dt
        self.widget_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        for y in range(0, pyray.get_render_height(), res.menu_bg_sprite.height):
            for x in range(0, pyray.get_render_width(), res.menu_bg_sprite.width):
                pyray.draw_texture_rec(res.menu_bg_sprite, self.bg_rect, pyray.Vector2(x, y), pyray.WHITE)
        self.widget_manager.draw()

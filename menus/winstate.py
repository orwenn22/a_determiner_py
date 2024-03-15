import pyray
from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton, info_widget
from utils import tiledbackground
import globalresources as res
from engine.tooltip import tooltip
from widgets import tiledwidget


class WinState(state.State):
    def __init__(self, winning_team: int, stats: dict):
        from menus import menustate
        super().__init__()

        def back_to_main_menu():
            self.manager.set_state(menustate.MenuState())

        self.tooltip = tooltip.Tooltip()

        self.widget_manager = widgetmanager.WidgetManager()
        
        return_menu = tiledbutton.TiledButton(0, 170, 270, 70, "MC", res.tiled_button_sprite, 8, 2, label="Return to main menu", act=back_to_main_menu)
        return_menu.set_font_color(pyray.WHITE).set_scrollable(False).center_text().set_hovering_color(pyray.YELLOW)

        winner_str = "Victory of blue team" if winning_team == 0 else "Victory of red team"
        winner_text = label.Label(0, -200, "MC", winner_str, 30, pyray.BLACK)

        stats_window = tiledwidget.TiledWidget(0, 0, 600, 350, "MC", res.tiled_button_sprite, 8, 2, label="Statistics")
        stats_window.set_offset_text(250, 20)
        # sprite will need to be changed when player indicator get merged | for now defaults will be used
        # now the interior of the stats window
        
        blue_team_label = label.Label(-150, -130, "MC", "Blue team :", 20, pyray.BLUE)
        red_team_label = label.Label(150, -130, "MC", "Red team : ", 20, pyray.RED)

        blue_shoot_number = label.Label(-150, -80, "MC", str(stats["shoot"][0]), 20, pyray.WHITE)
        red_shoot_number = label.Label(150, -80, "MC", str(stats["shoot"][1]), 20, pyray.WHITE)

        logo_shoot = info_widget.InfoWidget(0, -80, 40, 40, res.default_void_sprite, "Number of shot", self.tooltip, "MC")
        
        blue_jump_number = label.Label(-150, -30, "MC", str(stats["jump"][0]), 20, pyray.WHITE)
        red_jump_number = label.Label(150, -30, "MC", str(stats["jump"][1]), 20, pyray.WHITE)

        logo_jump = info_widget.InfoWidget(0, -30, 40, 40, res.default_void_sprite, "Number of jump", self.tooltip, "MC")
        
        blue_portal_number = label.Label(-150, 20, "MC", str(stats["portal"][0]), 20, pyray.WHITE)
        red_portal_number = label.Label(150, 20, "MC", str(stats["portal"][1]), 20, pyray.WHITE)

        logo_portal = info_widget.InfoWidget(0, 20, 40, 40, res.portal_gun_sprite, "Number of portal gun used", self.tooltip, "MC")

        blue_wall_number = label.Label(-150, 70, "MC", str(stats["wall"][0]), 20, pyray.WHITE)
        red_wall_number = label.Label(150, 70, "MC", str(stats["wall"][1]), 20, pyray.WHITE)

        logo_wall = info_widget.InfoWidget(0, 70, 40, 40, res.trowel_sprite, "Number of trowel used", self.tooltip, "MC")

        self.widget_manager.add_widget(stats_window)
        self.widget_manager.add_widget(blue_team_label)
        self.widget_manager.add_widget(red_team_label)
        self.widget_manager.add_widget(blue_shoot_number)
        self.widget_manager.add_widget(red_shoot_number)
        self.widget_manager.add_widget(logo_shoot)
        self.widget_manager.add_widget(blue_jump_number)
        self.widget_manager.add_widget(red_jump_number)
        self.widget_manager.add_widget(logo_jump)
        self.widget_manager.add_widget(blue_portal_number)
        self.widget_manager.add_widget(red_portal_number)
        self.widget_manager.add_widget(logo_portal)
        self.widget_manager.add_widget(blue_wall_number)
        self.widget_manager.add_widget(red_wall_number)
        self.widget_manager.add_widget(logo_wall)
        self.widget_manager.add_widget(return_menu)
        self.widget_manager.add_widget(winner_text)

        team_colors = [(50, 50, 255, 255), (255, 50, 50, 255)]
        self.bg = tiledbackground.TiledBackground(res.menu_bg_grayscale_sprite, team_colors[winning_team])

    def update(self, dt):
        self.bg.update(dt)
        self.tooltip.clear_elements()
        self.widget_manager.update(dt)

    def draw(self):
        self.bg.draw()
        self.widget_manager.draw()
        self.tooltip.draw(pyray.get_mouse_x(), pyray.get_mouse_y())
        

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
        
        back_button = tiledbutton.TiledButton(0, 170, 270, 70, "MC", res.tiled_button_sprite, 8, 2, label="Return to main menu", act=back_to_main_menu)
        back_button.set_font_color(pyray.WHITE).set_scrollable(False).center_text().set_hovering_color(pyray.YELLOW)

        winner_str = "Victory of blue team" if winning_team == 0 else "Victory of red team"
        winner_text = label.Label(0, -200, "MC", winner_str, 30, pyray.BLACK)

        stats_window = tiledwidget.TiledWidget(0, 0, 600, 350, "MC", res.tiled_button_sprite, 8, 2, label="Statistics")
        stats_window.set_offset_text(250, 20)
        self.widget_manager.add_widget(stats_window)
        # sprite will need to be changed when player indicator get merged | for now defaults will be used
        # now the interior of the stats window

        blue_team_label = label.Label(-150, -130, "MC", "Blue team :", 20, pyray.BLUE)
        red_team_label = label.Label(150, -130, "MC", "Red team : ", 20, pyray.RED)

        actions_sprites = [res.default_void_sprite, res.default_void_sprite, res.portal_gun_sprite, res.trowel_sprite]
        actions_names = ["shoot", "jump", "portal", "wall"]     # these must be the sames as gameplaystate.stats
        actions_descriptions = [                                # Descriptions for the tooltips
            "Number of shot",
            "Number of jump",
            "Number of portal gun used",
            "Number of trowel used"
        ]

        painter_y = -80
        for i in range(4):
            info_action = info_widget.InfoWidget(0, painter_y, 40, 40, actions_sprites[i], actions_descriptions[i], self.tooltip, "MC")
            red_stat = label.Label(-150, painter_y, "MC", str(stats[actions_names[i]][0]), 20, pyray.WHITE)
            blue_stat = label.Label(150, painter_y, "MC", str(stats[actions_names[i]][1]), 20, pyray.WHITE)
            self.widget_manager.add_widget(info_action)
            self.widget_manager.add_widget(red_stat)
            self.widget_manager.add_widget(blue_stat)
            painter_y += 50

        self.widget_manager.add_widget(blue_team_label)
        self.widget_manager.add_widget(red_team_label)
        self.widget_manager.add_widget(back_button)
        self.widget_manager.add_widget(winner_text)

        team_colors = [(100, 100, 255, 255), (255, 50, 50, 255)]
        self.bg = tiledbackground.TiledBackground(res.menu_bg_grayscale_sprite, team_colors[winning_team])

    def update(self, dt):
        self.bg.update(dt)
        self.tooltip.clear_elements()
        self.widget_manager.update(dt)

    def draw(self):
        self.bg.draw()
        self.widget_manager.draw()
        self.tooltip.draw(pyray.get_mouse_x(), pyray.get_mouse_y())
        

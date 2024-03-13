import pyray
from engine.state import state
from engine.widget import widgetmanager, label, tiledbutton, tiledwidget, info_widget
import globalresources as res
from engine.tooltip import tooltip


class WinState(state.State):
    def __init__(self,winning_team:int, stats: dict):
        from menus import menustate
        super().__init__()


        def back_to_main_menu():
            self.manager.set_state(menustate.MenuState())

        self.tooltip = tooltip.Tooltip()

        self.widget_manager = widgetmanager.WidgetManager()
        
        return_menu = tiledbutton.TiledButton(0, 70, 250, 70, "BC", res.tiled_button_sprite, 8, 2, label="Return to main menu", act=back_to_main_menu)
        return_menu.set_font_color(pyray.WHITE).set_scrollable(False).center_text().set_hovering_color(pyray.YELLOW)

        winner_str = "Victory of blue team" if winning_team == 0 else "Victory of red team"
        winner_text = label.Label(0, 50, "TC", winner_str, 28, pyray.BLACK)

        stats_window = tiledwidget.TiledWidget(0, 0, 600, 400, "MC", res.tiled_button_sprite,8,2, label="Statistics")
        stats_window.set_offset_text(250, 20)
        # sprite will need to be changed when player indicator get merged | for now defaults will be used
        # now the interior of the stats window
        
        blue_team_label = label.Label(-150,-150,"MC","Blue team :",20,pyray.BLUE)
        red_team_label = label.Label(150,-150,"MC","Red team : ",20,pyray.RED)

        blue_shoot_number = label.Label(-150, -100, "MC", str(stats["blue_shoot"]), 20, pyray.WHITE)
        red_shoot_number = label.Label(150, -100, "MC", str(stats["red_shoot"]), 20, pyray.WHITE)

        logo_shoot = info_widget.InfoWidget(0,-100,40,40,res.default_void_sprite,"Number of shot",self.tooltip,"MC")
        
        blue_jump_number = label.Label(-150, -50, "MC", str(stats["blue_jump"]), 20, pyray.WHITE)
        red_jump_number = label.Label(150, -50, "MC", str(stats["red_jump"]), 20, pyray.WHITE)

        logo_jump = info_widget.InfoWidget(0, -50, 40, 40, res.default_void_sprite, "Number of jump",self.tooltip ,"MC")
        
        blue_portal_number = label.Label(-150, 0, "MC", str(stats["blue_portal"]), 20, pyray.WHITE)
        red_portal_number = label.Label(150, 0, "MC", str(stats["red_portal"]), 20, pyray.WHITE)

        logo_portal = info_widget.InfoWidget(0, 0, 40, 40, res.portal_gun_sprite,"Number of portal gun used",self.tooltip, "MC")

        blue_wall_number = label.Label(-150, 50, "MC", str(stats["blue_wall"]), 20, pyray.WHITE)
        red_wall_number = label.Label(150, 50, "MC", str(stats["red_wall"]), 20, pyray.WHITE)

        logo_wall = info_widget.InfoWidget(0, 50, 40, 40, res.trowel_sprite, "Number of trowel used",self.tooltip,"MC")

        self.widget_manager.add_widget(return_menu)
        self.widget_manager.add_widget(winner_text)
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

        self.bg_rect = pyray.Rectangle(0, 0, res.menu_bg_sprite.width, res.menu_bg_sprite.height)

    def update(self, dt):
        self.bg_rect.x += 12*dt
        self.bg_rect.y += 12*dt
        self.tooltip.clear_elements()
        self.widget_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        for y in range(0, pyray.get_render_height(), res.menu_bg_sprite.height):
            for x in range(0, pyray.get_render_width(), res.menu_bg_sprite.width):
                pyray.draw_texture_rec(res.menu_bg_sprite, self.bg_rect, pyray.Vector2(x, y), pyray.WHITE)
        self.widget_manager.draw()
        self.tooltip.draw(pyray.get_mouse_x(),pyray.get_mouse_y() )
        

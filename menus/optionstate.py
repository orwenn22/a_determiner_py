import pyray
from engine.state import state
from engine.widget import button, widgetmanager, label
import globalresources as res
import key


class OptionState(state.State):
    def __init__(self):
        from menus import menustate
        super().__init__()

        def return_action():
            self.manager.set_state(menustate.MenuState())

        self.widget_manager = widgetmanager.WidgetManager()
        title = label.Label(0, -200, "MC",  "Options", 40, pyray.Color(0, 0, 0, 255))

        self.return_to_menu = button.Button(0, 200, 250, 40, "MC", return_action, "Return to main menu")

        # TODO : these should not be buttons
        self.key_left = button.Button(-50, -50, 140, 40, "MC", label="Left Key :")
        self.key_right = button.Button(-50, 0, 140, 40, "MC", label="Right Key :")
        self.key_action = button.Button(-50, 50, 140, 40, "MC", label="Action Key :")

        # All rebinds button should go here, and the key should be the same than the one in key.py
        self.rebind_buttons = {
            "left": button.Button(110, -50, 170, 40, "MC", self.make_newkey_callback("left"), "Q"),
            "right": button.Button(110, 0, 170, 40, "MC", self.make_newkey_callback("right"), "D"),
            "action": button.Button(110, 50, 170, 40, "MC", self.make_newkey_callback("action"), "SPACE")
        }

        # the key that is currently being rebinded
        self.rebinding = ""

        self.widget_manager.add_widget(self.return_to_menu)
        self.widget_manager.add_widget(title)
        self.widget_manager.add_widget(self.key_left)
        self.widget_manager.add_widget(self.rebind_buttons["left"])
        self.widget_manager.add_widget(self.key_right)
        self.widget_manager.add_widget(self.rebind_buttons["right"])
        self.widget_manager.add_widget(self.key_action)
        self.widget_manager.add_widget(self.rebind_buttons["action"])
        self.refresh_rebinding_buttons_labels()

        self.bg_rect = pyray.Rectangle(0, 0, res.menu_bg_option_sprite.width, res.menu_bg_option_sprite.height)

    def update(self, dt):
        self.bg_rect.x += 12 * dt
        self.bg_rect.y += 12 * dt
        if self.rebinding != "":
            for i in range(pyray.KeyboardKey.KEY_APOSTROPHE, pyray.KeyboardKey.KEY_PAUSE+1):
                if pyray.is_key_pressed(i):
                    key.key_binds[self.rebinding] = i
                    self.refresh_rebinding_buttons_labels()
                    self.rebinding = ""
                    break
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        for y in range(0, pyray.get_render_height(), res.menu_bg_sprite.height):
            for x in range(0, pyray.get_render_width(), res.menu_bg_sprite.width):
                pyray.draw_texture_rec(res.menu_bg_option_sprite, self.bg_rect, pyray.Vector2(x, y), pyray.WHITE)
        self.widget_manager.draw()

    def make_newkey_callback(self, key_to_change: str):
        def local_newkey_callback():
            self.rebinding = key_to_change
            self.refresh_rebinding_buttons_labels()
            if key_to_change not in self.rebind_buttons.keys():
                print("local_newkey_callback : no button with key", key_to_change)
                return
            self.rebind_buttons[key_to_change].label = ">PRESS<"
        return local_newkey_callback

    def refresh_rebinding_buttons_labels(self):
        for k, v in self.rebind_buttons.items():
            if k not in key.key_binds.keys():
                v.label = "N/A"
            else:
                v.label = list(pyray.KeyboardKey.__members__.keys())[list(pyray.KeyboardKey.__members__.values()).index(pyray.KeyboardKey(key.key_binds[k]))][4:]

import pyray
from engine.state import state
from engine.widget import tiledbutton, widgetmanager, label
from utils import tiledbackground
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

        key_left = tiledbutton.TiledButton(-85, -50, 140, 40, "MC",
                                           res.tiled_button_left_sprite, 8, 2,
                                           "Left Key :", self.make_newkey_callback("left"))
        key_left.center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        key_right = tiledbutton.TiledButton(-85, 0, 140, 40, "MC",
                                            res.tiled_button_left_sprite, 8, 2,
                                            "Right Key :", self.make_newkey_callback("right"))
        key_right.center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        key_action = tiledbutton.TiledButton(-85, 50, 140, 40, "MC",
                                             res.tiled_button_left_sprite, 8, 2,
                                             "Action Key :", self.make_newkey_callback("action"))
        key_action.center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        # All rebinds button should go here, and the key should be the same than the one in key.py
        self.rebind_buttons = {
            "left": tiledbutton.TiledButton(70, -50, 170, 40, "MC",
                                            res.tiled_button_right_sprite, 8, 2,
                                            "Q", self.make_newkey_callback("left")),
            "right": tiledbutton.TiledButton(70, 0, 170, 40, "MC",
                                             res.tiled_button_right_sprite, 8, 2,
                                             "D", self.make_newkey_callback("right")),
            "action": tiledbutton.TiledButton(70, 50, 170, 40, "MC",
                                              res.tiled_button_right_sprite, 8, 2,
                                              "SPACE", self.make_newkey_callback("action"))
        }

        for _, b in self.rebind_buttons.items():
            b.set_hovering_color(pyray.YELLOW)

        return_to_menu = tiledbutton.TiledButton(0, 200, 250, 40, "MC",
                                                 res.tiled_button_sprite, 8, 2,
                                                 "Return to main menu", return_action)
        return_to_menu.center_text().set_font_color(pyray.WHITE).set_hovering_color(pyray.YELLOW)

        self.widget_manager.add_widget(title)
        self.widget_manager.add_widget(key_left)
        self.widget_manager.add_widget(self.rebind_buttons["left"])
        self.widget_manager.add_widget(key_right)
        self.widget_manager.add_widget(self.rebind_buttons["right"])
        self.widget_manager.add_widget(key_action)
        self.widget_manager.add_widget(self.rebind_buttons["action"])
        self.widget_manager.add_widget(return_to_menu)
        self.refresh_rebinding_buttons_labels()

        self.bg = tiledbackground.TiledBackground(res.menu_bg_option_sprite)

        # the key that is currently being rebinded
        self.rebinding = ""

    def update(self, dt):
        self.bg.update(dt)
        if self.rebinding != "":
            for i in range(pyray.KeyboardKey.KEY_SPACE, pyray.KeyboardKey.KEY_PAUSE+1):
                if pyray.is_key_pressed(i):
                    key.key_binds[self.rebinding] = i
                    self.refresh_rebinding_buttons_labels()
                    self.rebinding = ""
                    break
        self.widget_manager.update(dt)

    def draw(self):
        self.bg.draw()
        self.widget_manager.draw()

    def make_newkey_callback(self, key_to_change: str):
        def local_newkey_callback():
            self.rebinding = key_to_change
            self.refresh_rebinding_buttons_labels()
            if key_to_change not in self.rebind_buttons.keys():
                print("local_newkey_callback : no button with key", key_to_change)
                return
            self.rebind_buttons[key_to_change].label = ">PRESS<"
            self.rebind_buttons[key_to_change].set_font_color(pyray.YELLOW).center_text()
        return local_newkey_callback

    def refresh_rebinding_buttons_labels(self):
        for k, v in self.rebind_buttons.items():
            if k not in key.key_binds.keys():
                v.label = "N/A"
                v.set_font_color(pyray.RED)
            else:
                v.label = list(pyray.KeyboardKey.__members__.keys())[list(pyray.KeyboardKey.__members__.values()).index(pyray.KeyboardKey(key.key_binds[k]))][4:]
                v.set_font_color(pyray.WHITE)
            v.center_text()

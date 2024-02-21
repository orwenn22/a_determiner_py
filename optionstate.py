import pyray
from engine.state import state
from engine.widget import button, widgetmanager
import menustate
import key


class OptionState(state.State):
    def __init__(self):
        super().__init__()

        def return_action():
            self.manager.set_state(menustate.MenuState())

        self.widget_manager = widgetmanager.WidgetManager()
        self.title = button.Button(50, -200, 250, 80, "MC", label="Options :")
        self.title.set_font_size(40).set_color(pyray.Color(0, 0, 0, 0)).set_font_color(pyray.Color(127, 127, 127, 255))

        self.returntomenu = button.Button(0, 200, 250, 40, "MC", return_action, "Return to main menu")

        # TODO : these are not buttons
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

        self.widget_manager.add_widget(self.returntomenu)
        self.widget_manager.add_widget(self.title)
        self.widget_manager.add_widget(self.key_left)
        self.widget_manager.add_widget(self.rebind_buttons["left"])
        self.widget_manager.add_widget(self.key_right)
        self.widget_manager.add_widget(self.rebind_buttons["right"])
        self.widget_manager.add_widget(self.key_action)
        self.widget_manager.add_widget(self.rebind_buttons["action"])

        self.refresh_rebinding_buttons_labels()

    def update(self, dt):
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

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


            # if you even let me do that, we should add another stop condition to the while loop (in the case we do it properly we should also create a class inputbutton)
        def newleftkey():
            pyray.poll_input_events()
            temp = 0
            while (not temp):
                temp = pyray.get_key_pressed()
                pyray.poll_input_events()
            if temp != 0 and temp != key.jkey_right:
                key.jkey_left = temp
                self.choice_key_left.label = list(pyray.KeyboardKey.__members__.keys())[
                    list(pyray.KeyboardKey.__members__.values()).index(pyray.KeyboardKey(temp))][4:]


        def newrightkey():
            pyray.poll_input_events()
            temp = 0
            while (not temp):
                temp = pyray.get_key_pressed()
                pyray.poll_input_events()
            if temp != 0 and temp != key.jkey_left:
                key.jkey_right = temp
                self.choice_key_right.label = list(pyray.KeyboardKey.__members__.keys())[
                    list(pyray.KeyboardKey.__members__.values()).index(pyray.KeyboardKey(temp))][4:]

        def newactionkey():
            pyray.poll_input_events()
            temp = 0
            while (not temp):
                temp = pyray.get_key_pressed()
                pyray.poll_input_events()
            if temp != 0 and temp != key.action_key:
                key.action_key = temp
                self.choice_key_action.label = list(pyray.KeyboardKey.__members__.keys())[
                    list(pyray.KeyboardKey.__members__.values()).index(pyray.KeyboardKey(temp))][4:]


        self.widget_manager = widgetmanager.WidgetManager()
        self.title = button.Button(50, -200, 250, 80, "MC", label="Options :")
        self.title.set_font_size(40).set_color(pyray.Color(0, 0, 0, 0)).set_font_color(pyray.Color(127, 127, 127, 255))

        self.returntomenu = button.Button(0, 200, 250, 40, "MC", return_action, "Return to main menu")

        self.key_left = button.Button(-50, -50, 140, 40, "MC", label="Left Key :")
        self.key_right = button.Button(-50, 0, 140, 40, "MC", label="Right Key :")
        self.key_action = button.Button(-50, 50, 140, 40, "MC", label="Action Key :")
        self.choice_key_left = button.Button(110, -50, 170, 40, "MC", newleftkey, "Q")
        self.choice_key_right = button.Button(110, 0, 170, 40, "MC", newrightkey, "D")
        self.choice_key_action = button.Button(110, 50, 170, 40, "MC", newactionkey, "SPACE")

        self.widget_manager.add_widget(self.returntomenu)
        self.widget_manager.add_widget(self.title)
        self.widget_manager.add_widget(self.key_left)
        self.widget_manager.add_widget(self.choice_key_left)
        self.widget_manager.add_widget(self.key_right)
        self.widget_manager.add_widget(self.choice_key_right)
        self.widget_manager.add_widget(self.key_action)
        self.widget_manager.add_widget(self.choice_key_action)

    def update(self, dt):
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()

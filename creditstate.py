import pyray
from engine.state import state
from engine.widget import button, widgetmanager


class CreditState(state.State):
    def __init__(self):
        super().__init__()
        self.widget_manager = widgetmanager.WidgetManager()

        self.title = button.Button(-50, -150, 250, 40, "MC", label="À déterminer tm")
        self.title.set_font_size(40).set_color(pyray.Color(0, 0, 0, 0)).set_font_color(pyray.Color(127, 127, 127, 255))

        self.group = button.Button(-30, -80, 250, 80, "MC", label="By : SomeGroup")
        self.group.set_font_size(30).set_color(pyray.Color(0, 0, 0, 0)).set_font_color(pyray.Color(127, 127, 127, 255))

        self.people = button.Button(-20, 0, 250, 150, "MC",
                                    label="- Ewenn Baudet\n\n- Alexis Delavis\n\n- Jude Aybalen\n\n- Adrian Noyes\n\n- Maxime Duret")

        self.widget_manager.add_widget(self.title)
        self.widget_manager.add_widget(self.group)
        self.widget_manager.add_widget(self.people)

    def update(self, dt):
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()

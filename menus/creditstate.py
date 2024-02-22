import pyray
from engine.state import state
from engine.widget import button, widgetmanager, label


class CreditState(state.State):
    def __init__(self):
        super().__init__()
        self.widget_manager = widgetmanager.WidgetManager()

        title = label.Label(0, -150, "MC", "À déterminer", 40, pyray.Color(127, 127, 127, 255))
        tm = label.Label(140, -160, "MC", "TM", 10, pyray.Color(127, 127, 127, 255))
        group = label.Label(0, -100, "MC", "By : SomeGroup", 30, pyray.Color(127, 127, 127, 255))

        people = button.Button(0, 0, 250, 150, "MC",
                               label="- Ewenn Baudet\n\n- Alexis Delavis\n\n- Jude Aybalen\n\n- Adrian Noyes\n\n- Maxime Duret")

        self.widget_manager.add_widget(title)
        self.widget_manager.add_widget(tm)
        self.widget_manager.add_widget(group)
        self.widget_manager.add_widget(people)

    def update(self, dt):
        self.widget_manager.update()

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()

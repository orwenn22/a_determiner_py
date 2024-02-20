import pyray
from engine.state import state
from engine.widget import button
import gameplaystate


class MenuState(state.State):
    def __init__(self):
        super().__init__()
        self.play = button.Button(-40, 0, 100, 40, "MC", self.play_action, "Play Game")

    def draw(self):
        self.play.draw()

    def play_action(self):
        self.manager.set_state(gameplaystate.GameplayState())

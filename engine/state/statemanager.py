from engine.state import state


class StateManager(object):
    def __init__(self, state: state.State = None):
        self.set_state(state)

    def set_state(self, state: state.State):
        self.state = state
        state.manager = self

    def update(self, dt: float):
        if state is not None:
            self.state.update(dt)

    def draw(self):
        if state is not None:
            self.state.draw()

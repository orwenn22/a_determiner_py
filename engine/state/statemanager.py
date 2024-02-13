from engine.state import state


class StateManager(object):
    def __init__(self, state: state.State = None):
        self.state = None
        self.old_state = None
        self.set_state(state)

    def unload(self):
        if self.state is not None:
            self.state.unload_ressources()
            self.state = None
        if self.old_state is not None:
            self.old_state.unload_ressources()
            self.old_state = None

    def set_state(self, state: state.State):
        self.old_state = self.state
        self.state = state
        state.manager = self

    def update(self, dt: float):
        if state is not None:
            self.state.update(dt)

        # We delay unloading ressources of the previous state, because if a state replace itself
        # the execution will still be inside of it.
        if self.old_state is not None:
            self.old_state.unload_ressources()
            self.old_state = None

    def draw(self):
        if state is not None:
            self.state.draw()

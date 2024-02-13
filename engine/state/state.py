class State(object):
    def __init__(self):
        from engine.state import statemanager
        self.manager: statemanager.StateManager = None

    def unload_ressources(self):
        pass

    def update(self, dt: float):
        pass

    def draw(self):
        pass

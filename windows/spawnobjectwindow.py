from engine.windows import window

from items import portalgun, trowel, spdiamond
from engine.widget import button


class SpawnObjectWindow(window.Window):
    def __init__(self, gameplay_state):
        super().__init__(10, 10, 200, 200)
        self.title = "Spawn collectible"
        self.background_color = (0, 0, 0, 127)
        self.title_bar_color = (25, 25, 200, 127)

        import gameplaystate
        self.gameplay_state: gameplaystate.GameplayState = gameplay_state

        # Each constructors in here must be like this : __init__(self, x, y)  (same as Collectible)
        self.constructors = [
            portalgun.PortalGun,
            trowel.Trowel,
            spdiamond.SPDiamond
        ]

        x = 2
        y = 2
        for i in range(len(self.constructors)):
            self.widget_manager.add_widget(button.Button(x, y, 20, 20, "LT", self.make_spawn_object_callback(i), f"{i}"))
            x += 22
            if x >= self.width-24:
                y += 22
                x = 2

    def make_spawn_object_callback(self, index: int):
        def spawn_object_callback():
            self.gameplay_state.spawned_object = self.constructors[index](0, 0)
        return spawn_object_callback

    def _close(self):
        self.gameplay_state.spawned_object = None
        super()._close()
import pyray
from engine.object import entityobject
from gameobject import player


class Collectible(entityobject.EntityObject):
    def __init__(self, x: float, y: float):
        super().__init__(x, y, 0.5, 0.5, None)

    def _setup_collectible(self, w: float, h: float, sprite: pyray.Texture):
        """
        Should be used by subclasses' constructors to define their size and sprite
        """
        self.sprite = sprite
        self.width = w
        self.height = h

    def update(self, dt: float):
        cols: list[player.Player] = self.manager.get_collision(self, player.Player)
        for p in cols:
            if self.on_collect(p):                  # If collecting was a success
                self.manager.remove_object(self)    # Remove the object
                return                              # Stop iterating

    def on_collect(self, p: player.Player) -> bool:
        """
        Should be redefined by subclasses. Can return False to cancel the collecting.
        Otherwise, should always return True.
        """
        return True

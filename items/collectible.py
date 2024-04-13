import pyray
from engine.object import entityobject


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

    # TODO : put update method here and have some kind of on_collect callback ?

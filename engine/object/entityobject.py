import pyray

from engine import graphics as gr, metrics as m


class EntityObject(object):
    def __init__(self, x: float, y: float, width: float, height: float, sprite: pyray.Texture = None):
        # TODO : find some other way to do this
        from engine.object.objectmanager import ObjectManager
        """
        :param x: x pos in meter (center of the object)
        :param y: y pos in meter (center of the object)
        :param width: width in meter
        :param height: height in meter
        :param sprite: non mandatory sprite
        """
        self.position = pyray.Vector2(
            float(x), float(y))     # position in m
        self.width = width
        self.height = height
        self.sprite: pyray.Texture = sprite
        self.manager: ObjectManager = None

    def update(self, dt: float):
        pass

    def draw(self):
        pass

    def get_rectangle(self) -> tuple[float, float, float, float]:
        """
        Get a rectangle (hitbox) of the object
        :return: a tuple (x,y,width,height)  TODO : implement our own rectangle type ?
        """
        return (self.position.x - self.width/2, self.position.y - self.height/2, self.width, self.height)

    def draw_hitbox(self):
        """
        This is intended for debugging purposes : draw the hitbox in red
        """
        x, y, w, h = self.get_rectangle()
        gr.draw_rectangle(x, y, w, h, (255, 0, 0), False)

        # Cross at the center of the object
        gr.draw_line(
            pyray.Vector2(self.position.x - w/4, self.position.y),
            pyray.Vector2(self.position.x + w/4, self.position.y),
            (255, 0, 0)
        )
        gr.draw_line(
            pyray.Vector2(self.position.x, self.position.y - h/4),
            pyray.Vector2(self.position.x, self.position.y + h/4),
            (255, 0, 0)
        )

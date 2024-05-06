import pyray

from engine.object import kinematicobject
from gameobject import portal
from engine import graphics as gr


class PortalRemoverBullet(kinematicobject.KinematicObject):
    def __init__(self, x: float, y: float, parent_state, enable_gravity: bool = False):
        import gameplaystate
        super().__init__(x, y, 0.25, 0.25, 15)
        self.enable_physics = True
        self.enable_gravity = enable_gravity
        self.parent_state: gameplaystate.GameplayState = parent_state

    def update(self, dt: float):
        self.process_physics(dt)

        # If we collide with a portal, remove it and its destination.
        cols: list[portal.Portal] = self.manager.get_collision(self, portal.Portal)
        if len(cols) >= 1:
            dest = cols[0].destination
            if dest is not None:
                self.manager.remove_object(dest)
            self.manager.remove_object(cols[0])
            self.manager.remove_object(self)

    def draw(self):
        gr.draw_circle(self.position, self.width/2, pyray.Color(200, 10, 10, 255))

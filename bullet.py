import pyray

from engine.object import kinematicobject
from engine import graphics as gr


class Bullet(kinematicobject.KinematicObject):
    def __init__(self, x: float, y: float, parent_state, thrower: kinematicobject.KinematicObject):
        import gameplaystate
        super().__init__(x, y, 0.25, 0.25, 5)
        self.enable_physics = True
        self.enable_gravity = True
        self.parent_state: gameplaystate.GameplayState = parent_state
        self.power = 2.0
        self.thrower: kinematicobject.KinematicObject = thrower

    def update(self, dt: float):
        import testobj
        need_explosion = False

        self.process_physics(dt)
        if self.parent_state.t.check_collision_rec(self.get_rectangle()):   # collide with terrain
            # TODO : instead of exploding rn, maybe we could create an "explosion" object that would handle an animation ?
            need_explosion = True

        collisions = self.manager.get_collision(self, testobj.TestObj)
        if len(collisions) >= 1:
            for obj in collisions:
                if obj != self.thrower:
                    self.parent_state.kill_player(obj)
                    need_explosion = True

        if need_explosion:
            self.parent_state.t.destroy_circle(self.position, self.power)
            self.parent_state.object_manager.remove_object(self)

    def draw(self):
        gr.draw_circle(self.position, self.width/2, pyray.Color(255, 255, 255, 255))

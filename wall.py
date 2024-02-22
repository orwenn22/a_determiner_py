import pyray
from engine.object import kinematicobject 
import globalresources as ges
from engine import graphics
import terrain

class Wall(kinematicobject.KinematicObject):
    def __init__(self,x:float,y:float,width:float,height:float,t : terrain.Terrain):
        sprite = ges.portal_gun_sprite #(only for testing)

        super().__init__(x,y,width,height,10000,sprite) # wall is really heavy and as such should fall really fast
        self.grounded = False
        self.terrain = t
    def draw(self):
        graphics.draw_rectangle(self.position.x-self.width/2,self.position.y-self.height/2,self.width,self.height,pyray.Color(127,127,127,255))        
    def update(self,dt:float):
        if self.grounded is False: 
            self.process_physics_y(dt)
            self.grounded = self.is_grounded()

    def is_grounded(self) -> bool:
        old_y = self.position.y
        self.position.y+=0.01
        result = self.terrain.check_collision_rec(self.get_rectangle(),True)
        self.position.y = old_y
        return result

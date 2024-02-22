import pyray
from engine.object import kinematicobject 
import globalresources as ges
from engine import graphics
import terrain

class Wall(kinematicobject.KinematicObject):
    def __init__(self,x:float,y:float,width:float,height:float,t : terrain.Terrain):
        sprite = ges.wall_sprite

        super().__init__(x,y,width,height,10000,sprite) # wall is really heavy and as such should fall really fast | it's false but this commentary will stay like that because it's fun
        self.grounded = False
        self.terrain = t
    def draw(self):
        graphics.draw_sprite_scale(self.sprite,self.get_rectangle())#self.sprite,(self.position.x-self.width/2,self.position.y-self.height/2,self.width,self.height))
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

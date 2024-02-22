from . import playeraction
import pyray
import wall
import player
from engine import globals as g
import key
from engine import metrics as m
from engine import graphics as gr
import math
from terrain import Terrain

class PlaceWallAction(playeraction.PlayerAction):
    def __init__(self,t : Terrain):
        super().__init__()
        self.action_name = "Wall\n(item)"
        self.terrain = t
        

    def on_update(self, _player : player.Player,dt:float):
        if g.is_key_pressed(key.key_binds["right"]):
            _player.throw_angle = 0
        elif g.is_key_pressed(key.key_binds["left"]):
            _player.throw_angle = math.pi
        self.on_draw(_player)
        if g.is_key_pressed(key.key_binds["action"]):
            print(_player.throw_angle)
            if _player.throw_angle==math.pi:
                w = wall.Wall(_player.position.x - 2,_player.position.y,0.5,1,self.terrain)    # should be 2 meters but not sure
            else :
                w = wall.Wall(_player.position.x + 2,_player.position.y,0.5,1,self.terrain)    # should be 2 meters but not sure
            _player.manager.add_object(w) 
            print(_player.manager.list_object)
            _player.remove_action(self)
            _player.current_action = -1
            _player.parent_state.show_action_widgets()
            _player.throw_angle = 0
    def on_draw(self, _player: player.Player):
        if _player.throw_angle==math.pi:
            gr.draw_circle(pyray.Vector2(_player.position.x - 2,_player.position.y),0.1,pyray.Color(0,0,255,255))
        else:
            gr.draw_circle(pyray.Vector2(_player.position.x + 2,_player.position.y),0.1,pyray.Color(0,0,255,255))

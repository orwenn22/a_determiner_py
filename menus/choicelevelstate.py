import pyray
from engine.state import state
from engine.widget import widgetmanager, label, split_tiledbutton
import os
import gameplaystate
from engine import globals as g
import globalresources as res

class ChoiceLevelState(state.State):
    def __init__(self):
        super().__init__()

        self.list_level_file:list[str] = os.listdir("maps/")
        self.list_preview : list[pyray.Texture] = []

        #the next two variables are only there to detect if we should be able to scroll or no
        self.top_button_y=-400
        self.down_button_y=self.top_button_y+len(self.list_level_file)*120
        
        self.title_widget_manager = widgetmanager.WidgetManager()   # it's the best way i found to let the label set it's placement itself without being with the other widgets which supports scrolling but it can probably be done another way
        
        self.widget_manager = widgetmanager.WidgetManager()
        self.title = label.Label(0,0,"TC","Choose the level",30)
        self.title_widget_manager.add_widget(self.title)

        for i in range(1,len(self.list_level_file)+1):
            if self.list_level_file[i-1][:-4]+"_preview.png" in os.listdir("preview/"):
                self.list_preview.append(pyray.load_texture("preview/"+self.list_level_file[i-1][:-4]+"_preview.png"))
            else:
                self.list_preview.append(pyray.load_texture("res/default.png")) # loading the preview
                        
            self.widget_manager.add_widget(split_tiledbutton.SplitTiledButton(0,-400+i*120,300,100,"MC",res.tiled_button_sprite,8,self.list_preview[i-1],1,self.list_level_file[i-1][:-4],act=self.make_play_action(i)))
    
        #TODO: maybe change the background to something like in the other parts of the menu

    def update(self,dt):
        self.widget_manager.update()
        if g.mouse_wheel < 0 and self.down_button_y > pyray.get_screen_height()/2:      # the pyray.get_screen_height()/2 is necessary as the center is 0 and not the top
            self.top_button_y -= 120
            self.down_button_y -= 120
            for i in self.widget_manager.list_widget:
                i.coordinate.y -= 120
        if g.mouse_wheel > 0 and self.top_button_y < -400:
            self.top_button_y += 120
            self.down_button_y += 120
            for i in self.widget_manager.list_widget:
                i.coordinate.y += 120
        self.title_widget_manager.update() 

    def draw(self):
        pyray.clear_background(pyray.BLACK)
        self.widget_manager.draw()
        self.title_widget_manager.draw()

    def make_play_action(self,map_number : int = 1):
        def local_play_action():
            for i in self.list_preview:
                pyray.unload_texture(i)
            self.manager.set_state(gameplaystate.GameplayState(self.list_level_file[map_number-1]))
        return local_play_action

from engine.state import state
from engine.object import objectmanager
from engine.widget import widgetmanager
from engine import metrics as m, graphics as gr, globals as g, utils as u
from widgets import playersindicator
import pyray
from gameobject import player
import terrain
import mapparsing
from menus import winstate
import globalresources as res


class GameplayState(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit/zoom
        m.set_pixels_per_meter(50)

        # This is where we put permanent ui elements
        self.overlay = widgetmanager.WidgetManager()
        self.overlay.add_widget(playersindicator.PlayersIndicator(self))

        # Widget manager for the action buttons.
        self.actions_widgets = widgetmanager.WidgetManager()
        self.show_actions = False

        # We put all the players in here. This is to keep track of the order are the turns.
        # If a player dies, its entry in here should be set to None.
        # (use kill_player)
        self.players: list[player.Player | None] = []

        # This indicates if we are at the begging of the game, and we are currently placing players.
        self.placing_players = True

        # Indicate what player is currently playing
        self.current_player = -1

        # This will contain all the objects of the game
        self.object_manager = objectmanager.ObjectManager()

        # These are used for drag&dropping the camera
        self.cam_follow_mouse = False
        self.cam_mouse_offset = (0, 0)

        self.t: terrain.Terrain | None = None
        self.blue_start: tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0)
        self.red_start: tuple[float, float, float, float] = (0.0, 0.0, 1.0, 1.0)


        self.stats = {"red_jump":0, "blue_jump":0, "red_shoot":0, "blue_shoot":0, "red_portal":0, "blue_portal":0, "red_wall":0, "blue_wall":0 }

    def unload_ressources(self):
        self.t.unload()

    def update(self, dt):
        if self.t is None:
            print("Terrain not initialised, loading default")
            self.t = terrain.Terrain("level2.png", pyray.Vector2(25, 12))
            self.blue_start = (0, 0, 25, 12)
            self.red_start = (0, 0, 25, 12)
            return

        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()

        self.overlay.update(dt)

        if self.show_actions:
            self.actions_widgets.update(dt)                     # Check if we are clicking on an action

        self.update_cam_position(mouse_x, mouse_y)      # Camera drag&drop update

        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        self.t.update()
        self.object_manager.update(dt)                  # Update all objects
        if self.placing_players:                        # Check if we are still placing players
            gr.draw_rectangle(self.blue_start[0],self.blue_start[1],self.blue_start[2],self.blue_start[3],pyray.Color(0,0,255,90))
            gr.draw_rectangle(self.red_start[0],self.red_start[1],self.red_start[2],self.red_start[3],pyray.Color(255,0,0,90))
            self.place_player(mouse_pos_meter.x, mouse_pos_meter.y, len(self.players) % 2)

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        if self.t is None:
            pyray.draw_text("Terrain not initialised", 50, 50, 40, pyray.RED)
            return

        self.t.draw()
        #gr.draw_grid()
        self.object_manager.draw()
        if self.show_actions:
            self.actions_widgets.draw()

        self.overlay.draw()

        if self.current_player != -1:
            # Display green marker on top of current player
            player_pos = self.players[self.current_player].position
            arrow_pos = pyray.Vector2(player_pos.x, player_pos.y)
            arrow_pos.y -= 1
            gr.draw_sprite_rot(res.green_marker_sprite, arrow_pos, pyray.Vector2(0.5, 0.5), 0.0)

            # Display action points (this is temporary, we need to find a way to do this in a better way)
            arrow_pos.y -= 1
            text_pos = m.meters_position_to_window_position(arrow_pos)
            pyray.draw_text(str(self.players[self.current_player].action_points), int(
                text_pos.x), int(text_pos.y), 20, pyray.Color(255, 255, 255, 255))

    def update_cam_position(self, mouse_x: int, mouse_y: int):
        # Drag & drop cam
        if g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_RIGHT):
            self.cam_follow_mouse = True
            self.cam_mouse_offset = (m.x_offset_pixel - mouse_x, m.y_offset_pixel - mouse_y)
        if not g.is_mouse_button_down(pyray.MouseButton.MOUSE_BUTTON_RIGHT):
            self.cam_follow_mouse = False
        if self.cam_follow_mouse:
            m.x_offset_pixel = self.cam_mouse_offset[0] + mouse_x
            m.y_offset_pixel = self.cam_mouse_offset[1] + mouse_y
        else:
            # Zoom (we can't zoom while dragging)
            cam_center = m.get_camera_center()
            if g.mouse_wheel > 0:
                m.set_pixels_per_meter(m.pixels_per_meter * 2)
            elif g.mouse_wheel < 0:
                m.set_pixels_per_meter(m.pixels_per_meter // 2)
            m.set_camera_center(cam_center)

    def place_player(self, dest_x: float, dest_y: float, team: int):
        """
        Place a new player in the game, and add it to the player list
        :param dest_x: x destination in meter
        :param dest_y: y destination in meter
        """
        if not g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT) or g.mouse_used:
            return

        p = player.Player(dest_x, dest_y, team, self, 10)
        if self.t.check_collision_rec(p.get_rectangle(), True):     # Check if object is clipping in terrain
            return  # object clipping in terrain, we can't spawn it.
        if team == 0:
            if not u.check_collision_rectangles(p.get_rectangle(), self.blue_start):
                return
        else:
            if not u.check_collision_rectangles(p.get_rectangle(), self.red_start):
                return

        self.players.append(p)              # Add new player to player list
        self.object_manager.add_object(p)   # Add new player to objects
        print("object spawned at", p.position.x, p.position.y)
        if len(self.players) >= 6:          # Check if we are done manually spawning players
            self.placing_players = False
            self.next_player_turn()

    def kill_player(self, player_object: player.Player):
        """
        Kill a player.
        Player should be removed from the game only using this method, and nothing else.
        """
        p_index = -1
        for i in range(len(self.players)):
            if self.players[i] == player_object:
                p_index = i
                break

        if p_index == -1:
            return      # Object not found

        print("Killing player", p_index)
        self.players[p_index] = None
        self.object_manager.remove_object(player_object)
        
        red, blue = 0,0
        for i in range(len(self.players)):
            if self.players[i] is None:
                continue
            if self.players[i].team == 0:
                blue+=1
            elif self.players[i].team == 1:
                red+=1
        
        if blue <= 0:
            self.manager.set_state(winstate.WinState(1, self.stats))
        elif red <= 0:
            self.manager.set_state(winstate.WinState(0, self.stats))

        if p_index == self.current_player:
            self.next_player_turn()     # this is in the case the current player died :(

    def next_player_turn(self):
        """
        This will go to the next player's turn and display his actions
        """
        self.current_player += 1
        self.current_player %= len(self.players)

        # We don't want to give the turn to a dead player
        while self.players[self.current_player] is None:
            self.current_player += 1
            self.current_player %= len(self.players)

        for p in self.players:
            if p is not None:
                p.is_playing = 0

        self.players[self.current_player].is_playing = 1
        print("player", self.current_player)
        self.show_action_widgets()

    def show_action_widgets(self):
        """
        This will display the on-screen control buttons for the current object
        """
        self.actions_widgets.clear()
        self.show_actions = True
        marge = 10

        current_player = self.players[self.current_player]
        if current_player is None:
            return

        widgets = current_player.get_action_widgets()
        if len(widgets) == 0:
            return

        # Get width of all widget combined
        widgets_width = 0
        for w in widgets:
            widgets_width += w.width
        widgets_width += marge * (len(widgets)-1)                   # Add marge

        # Display all the widgets
        x_pos = -widgets_width//2 + widgets[0].width//2
        for i in range(len(widgets)-1):
            widgets[i].set_position(x_pos, marge)
            self.actions_widgets.add_widget(widgets[i])
            x_pos += (widgets[i].width + widgets[i+1].width)//2 + marge
        widgets[-1].set_position(x_pos, marge)
        self.actions_widgets.add_widget(widgets[-1])

    def hide_action_widgets(self):
        self.actions_widgets.clear()
        self.show_actions = False

    @classmethod
    def from_level_file(cls, level_file: str):
        r = cls()
        mapparsing.parse_map_file(r, level_file)
        return r

from engine.state import state
from engine.object import objectmanager
from engine.widget import widgetmanager, button
from engine import metrics as m, graphics as gr, globals as g
import pyray
import player
import terrain
import portal
import portalgun
import trowel

class GameplayState(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit/zoom
        m.set_pixels_per_meter(50)

        # Put the cam at the center of the world
        m.set_camera_center(pyray.Vector2(0, 0))

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

        # Terrain for collisions & stuff
        self.t = terrain.Terrain("level2.png", pyray.Vector2(25, 12))

        # Small marker for the current player
        self.green_marker = pyray.load_texture("res/green_marker.png")

        # These are used for drag&dropping the camera
        self.cam_follow_mouse = False
        self.cam_mouse_offset = (0, 0)

        portal.Portal.spawn_portals(self.object_manager, 5, 4, 9, 5, None)
        portal.Portal.spawn_portals(self.object_manager, 4, 2, 12, 4, None)
        self.object_manager.add_object(portalgun.PortalGun(23.3, 7.1))
        self.object_manager.add_object(trowel.Trowel(23.3, 6.1))

    def unload_ressources(self):
        self.t.unload()
        pyray.unload_texture(self.green_marker)

    def update(self, dt):
        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()
        if self.show_actions:
            self.actions_widgets.update()                   # Check if we are clicking on an action

        self.update_cam_position(mouse_x, mouse_y)      # Camera drag&drop update

        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        self.t.update()
        self.object_manager.update(dt)                  # Update all objects
        if self.placing_players:                        # Check if we are still placing players
            self.place_player(mouse_pos_meter.x, mouse_pos_meter.y, len(self.players) % 2)

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        self.t.draw()
        gr.draw_grid()
        self.object_manager.draw()
        if self.show_actions:
            self.actions_widgets.draw()

        if self.current_player != -1:
            # Display green marker on top of current player
            player_pos = self.players[self.current_player].position
            arrow_pos = pyray.Vector2(player_pos.x, player_pos.y)
            arrow_pos.y -= 1
            gr.draw_sprite_rot(self.green_marker, arrow_pos, pyray.Vector2(0.5, 0.5), 0.0)

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
        # TODO : implement spawn regions for each teams ?
        if not g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            return

        p = player.Player(dest_x, dest_y, team, self, 10)
        if self.t.check_collision_rec(p.get_rectangle(), True):     # Check if object is clipping in terrain
            return  # object clipping in terrain, we can't spawn it.

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

        self.players[p_index] = None
        self.object_manager.remove_object(player_object)
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

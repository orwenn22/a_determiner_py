import os
import pyray
import random

from engine.state import state
from engine.object import objectmanager
from engine.tooltip import tooltip
from engine.widget import widgetmanager, label
from engine.windows import windowmanager, window
from engine import metrics as m, graphics as gr, globals as g, utils as u
from widgets import playersindicator
from gameobject import player
from items import collectible
import terrain
import mapparsing
from menus import winstate, pausemenu
import globalresources as res
from windows import spawnobjectwindow
from items import spdiamond, trowel, portalgun, portalremover, strengthmodifier, hotpotato


# Team indexes :
#  1 : blue
#  2 : red

class GameplayState(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit/zoom
        m.set_pixels_per_meter(50)

        # This is where we put permanent ui elements
        self.overlay = widgetmanager.WidgetManager()
        self.overlay.add_widget(playersindicator.PlayersIndicator(self))
        self.hotbar_text = label.Label(0, 95, "BC", "Hotbar text", 20)
        self.hotbar_text.enable_outline = True
        self.overlay.add_widget(self.hotbar_text)

        # Widget manager for the action buttons.
        self.actions_widgets = widgetmanager.WidgetManager()

        # This is where we put all the windows
        self.window_manager = windowmanager.WindowManager()
        self.spawned_object: collectible.Collectible | None = None

        # This is set to True if show_action_widgets is called, and to False when hide_action_widgets is called.
        self.show_actions = False

        # We put all the players in here. This is to keep track of the order are the turns.
        # If a player dies, its entry in here should be set to None.
        # (use kill_player)
        self.players: list[player.Player | None] = []

        # Indicate what player is currently playing (-1 means we are still placing players at the beginning of the game)
        self.current_player = -1
        self.players_per_team = 3       # TODO : make this configurable in settings ??

        # This will contain all the objects of the game
        self.object_manager = objectmanager.ObjectManager()

        # Tooltip to put info when hovering on some elements
        self.tooltip = tooltip.Tooltip()

        # These are used for drag&dropping the camera
        self.cam_follow_mouse = False
        self.cam_mouse_offset = (0, 0)

        # The terrain is set to None by default. It should be initialised before we call update or draw
        self.t: terrain.Terrain | None = None

        # Spawn region of each teams
        self.starts: list[tuple[float, float, float, float]] = [
            (0.0, 0.0, 1.0, 1.0),       # Blue
            (0.0, 0.0, 1.0, 1.0)        # Red
        ]

        # Colors associated to each team (alpha of 90 because they are used for drawing the spawn regions)
        self.team_colors: list[pyray.Color] = [
            pyray.Color(0, 0, 255, 90),
            pyray.Color(255, 0, 0, 90)
        ]

        # Stats for each teams
        self.stats = {
            "jump": [0, 0],
            "shoot": [0, 0],
            "portal": [0, 0],
            "wall": [0, 0]
        }

    def unload_ressources(self):
        if self.t is not None:
            self.t.unload()

    def initialise_terrain(self, bitmap_path: str, width_m: float, height_m: float):
        """
        Load a terrain into the gameplay state
        """
        if not os.path.isfile(bitmap_path):
            print("initialise_terrain : path " + bitmap_path + " don't exist :(")

        if self.t is not None:
            self.t.unload()
        self.t = terrain.Terrain(bitmap_path, pyray.Vector2(width_m, height_m))
        print("initialise_terrain : Successfully loaded " + bitmap_path + "as bitmap")

    def update(self, dt):
        self.tooltip.clear_elements()

        if g.is_key_pressed(pyray.KeyboardKey.KEY_ESCAPE):
            self.manager.set_state(pausemenu.PauseMenu(self), False)    # We don't want to unload the map yet
            return

        if self.t is None:
            print("Terrain not initialised, loading default")
            self.initialise_terrain("maps/old/level1.png", 25.0, 12.0)
            self.starts[0] = (0, 0, 25, 12)
            self.starts[1] = (0, 0, 25, 12)
            return

        if g.is_key_pressed(pyray.KeyboardKey.KEY_F1):
            if not self.window_manager.check_existence(spawnobjectwindow.SpawnObjectWindow):
                self.window_manager.add_window(spawnobjectwindow.SpawnObjectWindow(self))

        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()

        self.window_manager.update(dt)
        self.overlay.update(dt)

        if self.show_actions:
            self.actions_widgets.update(dt)                     # Check if we are clicking on an action

        self.update_cam_position(mouse_x, mouse_y)      # Camera drag&drop update

        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)

        self.update_spawned_object(mouse_pos_meter)

        self.t.update()
        self.object_manager.update(dt)                  # Update all objects
        if self.placing_players():                      # Check if we are still placing players
            self.place_player(mouse_pos_meter.x, mouse_pos_meter.y, len(self.players) % 2)

        self.update_hotbar_text()

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))

        # Show the spawn regions if we are placing players
        if self.placing_players():
            for i in range(len(self.starts)):
                gr.draw_rectangle(self.starts[i][0], self.starts[i][1], self.starts[i][2], self.starts[i][3], self.team_colors[i])

        if self.t is None:
            pyray.draw_text("Terrain not initialised", 50, 50, 40, pyray.RED)
            return

        self.t.draw()
        #gr.draw_grid()
        self.object_manager.draw()

        if g.is_key_down(pyray.KeyboardKey.KEY_F2):
            return

        if not self.placing_players():
            # Display green marker on top of current player
            player_pos = self.get_current_player().position
            arrow_pos = pyray.Vector2(player_pos.x, player_pos.y)
            arrow_pos.y -= 1
            gr.draw_sprite_rot(res.green_marker_sprite, arrow_pos, pyray.Vector2(0.5, 0.5), 0.0)

        if self.spawned_object is not None and not g.mouse_used:
            self.spawned_object.draw()

        if self.show_actions:
            self.actions_widgets.draw()

        self.overlay.draw()

        self.window_manager.draw()
        self.tooltip.draw(pyray.get_mouse_x()+6, pyray.get_mouse_y()+6)

    def update_cam_position(self, mouse_x: int, mouse_y: int):
        # Drag & drop cam
        if g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_RIGHT) and not g.mouse_used:
            self.cam_follow_mouse = True
            self.cam_mouse_offset = (m.x_offset_pixel - mouse_x, m.y_offset_pixel - mouse_y)
        if not g.is_mouse_button_down(pyray.MouseButton.MOUSE_BUTTON_RIGHT):
            self.cam_follow_mouse = False
        if self.cam_follow_mouse:
            m.x_offset_pixel = self.cam_mouse_offset[0] + mouse_x
            m.y_offset_pixel = self.cam_mouse_offset[1] + mouse_y
        else:
            if g.mouse_used:
                return
            # Zoom (we can't zoom while dragging)
            cam_center = m.get_camera_center()
            if g.mouse_wheel > 0:
                m.set_pixels_per_meter(m.pixels_per_meter * 2)
            elif g.mouse_wheel < 0:
                m.set_pixels_per_meter(m.pixels_per_meter // 2)
            m.set_camera_center(cam_center)

    def update_spawned_object(self, mouse_pos_meter: pyray.Vector2):
        """
        Update the object spawned using the cheat window
        """
        if self.spawned_object is None:
            return

        self.spawned_object.position.x = mouse_pos_meter.x
        self.spawned_object.position.y = mouse_pos_meter.y
        if g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT) and not g.mouse_used:
            g.mouse_used = True
            self.object_manager.add_object(self.spawned_object)
            self.spawned_object = None

    def update_hotbar_text(self):
        """
        This will put the default messages in the hotbar text depending on the situation
        """
        # Currently this get executed at every frame, therefore it is not optimised at all.
        if self.current_player == -1:
            team_name = "blue" if len(self.players) % 2 == 0 else "red"
            self.hotbar_text.set_text(f"Place {team_name} player")
            self.hotbar_text.set_color(pyray.BLUE if len(self.players) % 2 == 0 else pyray.RED)
            return

        p = self.get_current_player()
        if p is None:
            self.hotbar_text.set_text("Error : player is None :^(")
            return

        self.hotbar_text.set_text(f"Energy : {p.action_points}")
        self.hotbar_text.set_color(pyray.BLUE if p.team == 0 else pyray.RED)

    def place_player(self, dest_x: float, dest_y: float, team: int, check_start_pos: bool = True):
        """
        Place a new player in the game, and add it to the player list
        :param dest_x: x destination in meter
        :param dest_y: y destination in meter
        :param team: the team of the player (0 for blue, 1 for red)
        :param check_start_pos: if set to true, we will check if the player is spawned in its team's associated region
        """
        if not g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT) or g.mouse_used:
            return

        p = player.Player(dest_x, dest_y, team, self, 10)
        if self.t.check_collision_rec(p.get_rectangle(), True):     # Check if object is clipping in terrain
            return  # object clipping in terrain, we can't spawn it.

        if not u.check_collision_rectangles(p.get_rectangle(), self.starts[team]) and check_start_pos:
            return

        self.players.append(p)              # Add new player to player list
        self.object_manager.add_object(p)   # Add new player to objects
        print("object spawned at", p.position.x, p.position.y)
        if len(self.players) >= self.players_per_team*2:          # Check if we are done manually spawning players
            self.next_player_turn()

    def placing_players(self) -> bool:
        """
        Return true if we are still placing players, false otherwise.
        """
        return self.current_player == -1

    def get_current_player(self) -> None | player.Player:
        """
        Return a ref to the player that is currently playing (None if there are no player)
        """
        if self.current_player < 0 or self.current_player >= len(self.players):
            return None
        return self.players[self.current_player]

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
        
        self.check_victory()

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

        if random.random() < 0.20:      # 20% chance of spawning random items
            item_count = random.randint(1, 5)
            for i in range(item_count): self.spawn_item_randomly()

        print("player", self.current_player, "'s turn")
        self.show_action_widgets()

    def show_action_widgets(self):
        """
        This will display the on-screen control buttons for the current object
        (this will clear the previous action buttons if they exist)
        """
        self.actions_widgets.clear()
        self.show_actions = True
        marge = 10

        current_player = self.get_current_player()
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

    def check_victory(self):
        # Count the number of remaining players in each team
        team_counts = [0, 0]
        for i in range(len(self.players)):
            if self.players[i] is None:
                continue
            team_counts[self.players[i].team] += 1
        print(team_counts)

        # Look if there is only one team where there are players alive
        # (this is like this to make it easier in the case we add more teams)
        victory_index = -1
        for i in range(len(team_counts)):
            if team_counts[i] > 0:
                if victory_index == -1:
                    victory_index = i
                else:       # 2 teams have players alive, stop here
                    victory_index = -1
                    break

        # Display end screen if necessary
        if victory_index != -1:
            print("Victory of team", victory_index)
            self.manager.set_state(winstate.WinState(victory_index, self.stats))

    def spawn_item_randomly(self):
        random_x = random.random() * self.t.size.x
        random_y = random.random() * self.t.size.y

        # Constructors of all the objects
        items = [
            spdiamond.SPDiamond,
            trowel.Trowel,
            portalgun.PortalGun,
            portalremover.PortalRemover,
            strengthmodifier.StrengthModifier.make_upgrade,
            strengthmodifier.StrengthModifier.make_downgrade,
            hotpotato.HotPotato
        ]
        random_item_index = random.randint(0, len(items)-1)

        item = items[random_item_index](random_x, random_y)

        if self.t.check_collision_rec(item.get_rectangle(), True):        # the objet is clipping inside the terrain
            iterations = 0
            while self.t.check_collision_rec(item.get_rectangle(), True):
                item.position.y -= 0.1      # Make it go up
                iterations += 1
                if iterations > 1500:
                    self.spawn_item_randomly()      # In that case we might be in an impossible situation, so try again
                    return                          # Don't spawn the bad item
        else:           # Not clipping terrain
            while not self.t.check_collision_rec(item.get_rectangle(), True):
                item.position.y += 0.1  # Make it go down
            item.position.y -= 0.2      # When we find the floor, make it go up

        # Make it so we can't randomly spawn the item on a player
        if self.object_manager.get_collision(item, player.Player):
            print("spawn_item_randomly : spawning item on player, cancelling")
            # recursive call here ?
            return

        self.object_manager.add_object(item)

    @classmethod
    def from_level_file(cls, level_file: str):      # Returns gameplaystate or None
        r = cls()
        error_mes = mapparsing.parse_map_file(r, level_file)
        if error_mes != "":
            print("Error parsing map : " + error_mes)
            return None
        return r

from engine.state import state
from engine.object import objectmanager
from engine.widget import widgetmanager, button
from engine import metrics as m, graphics as gr, globals as g
import pyray
import testobj
import terrain


class GameplayState(state.State):
    def __init__(self):
        super().__init__()

        # Set the unit
        m.set_pixels_per_meter(50)

        # Put the cam at the center of the world
        m.set_camera_center(pyray.Vector2(0, 0))

        self.widget_manager = widgetmanager.WidgetManager()

        # We put all the players in here. This is to keep track of the order are the turns.
        self.players: list[testobj.TestObj] = []
        self.placing_players = True
        self.current_player = -1        # Indicate what player is currently playing

        # create a manager with some objects in it
        self.object_manager = objectmanager.ObjectManager()
        # self.object_manager.add_object(testobj.TestObj(1, 1, 0, self))
        # self.object_manager.add_object(testobj.TestObj(3, 1,  1, self, 20))

        self.t = terrain.Terrain("level2.png", pyray.Vector2(25, 12))
        self.green_marker = pyray.load_texture("green_marker.png")

        self.cam_follow_mouse = False
        self.cam_mouse_offset = (0, 0)

    def unload_ressources(self):
        self.t.unload()
        pyray.unload_texture(self.green_marker)

    def update(self, dt):
        mouse_x, mouse_y = pyray.get_mouse_x(), pyray.get_mouse_y()

        self.widget_manager.update()

        self.update_cam_position(mouse_x, mouse_y)

        mouse_pos_meter = m.window_position_to_meters_position(mouse_x, mouse_y)
        if g.is_key_down(pyray.KeyboardKey.KEY_B):
            self.t.destroy_circle(mouse_pos_meter, 1)

        self.t.update()

        if self.placing_players:    # Technicaly this check isn't necessary, but let's do it anyway to prevent future mistakes.
            self.place_player(mouse_pos_meter.x, mouse_pos_meter.y)

        self.object_manager.update(dt)

    def draw(self):
        pyray.clear_background(pyray.Color(25, 25, 25, 255))
        self.t.draw()
        gr.draw_grid()
        self.object_manager.draw()
        self.widget_manager.draw()

        if self.current_player != -1:
            # Display green marker on top of current player
            player_pos = self.players[self.current_player].position
            arrow_pos = pyray.Vector2(player_pos.x, player_pos.y)
            arrow_pos.y -= 1
            gr.draw_sprite_rot(self.green_marker, arrow_pos, pyray.Vector2(0.5, 0.5), 0.0)

            # Display action points
            arrow_pos.y -= 1
            text_pos = m.meters_position_to_window_position(arrow_pos)
            pyray.draw_text(str(self.players[self.current_player].action_points), int(text_pos.x), int(text_pos.y), 20, pyray.Color(255, 255, 255, 255))

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

    def place_player(self, mouse_x: float, mouse_y: float):
        if not self.placing_players or not g.is_mouse_button_pressed(pyray.MouseButton.MOUSE_BUTTON_LEFT):
            return

        placing_team = len(self.players)%2
        p = testobj.TestObj(mouse_x, mouse_y, placing_team, self, 10)
        if self.t.check_collision_rec(p.get_rectangle()):
            return  # object clipping in terrain, we can't spawn it.

        self.players.append(p)
        self.object_manager.add_object(p)
        print("object spawned at", p.position.x, p.position.y)
        if len(self.players) == 6:
            self.placing_players = False
            self.next_player_turn()

    def next_player_turn(self):
        """
        This will go to the next player's turn
        """
        self.current_player += 1
        self.current_player %= len(self.players)

        for p in self.players:
            p.action = 0

        self.players[self.current_player].action = 1
        print("player", self.current_player)
        self.show_action_widgets()

    def show_action_widgets(self):
        """
        This will display the on-screen control buttons
        """
        self.widget_manager.clear()

        # Declare the actions of each buttons
        def local_setaction_jump():
            self.players[self.current_player].action = 2

        def local_setaction_shoot():
            self.players[self.current_player].action = 3

        def local_skip_turn():
            self.players[self.current_player].action_points += 10
            self.next_player_turn()

        button_size = 64
        marge = 10
        button_count = 3
        print(button_count*button_size + (button_count-1)*marge)
        x_pos = -(button_count*button_size + (button_count-1)*marge)//2 + button_size//2

        button_jump = button.Button(x_pos, marge, button_size, button_size, "BC", local_setaction_jump, "JUMP")
        self.widget_manager.add_widget(button_jump)

        x_pos += button_size + marge

        button_shoot = button.Button(x_pos, marge, button_size, button_size, "BC", local_setaction_shoot, "SHOOT")
        self.widget_manager.add_widget(button_shoot)

        x_pos += button_size + marge

        button_skip_turn = button.Button(x_pos, marge, button_size, button_size, "BC", local_skip_turn, "SKIP")
        self.widget_manager.add_widget(button_skip_turn)

import pyray

from engine.windows import window


class WindowManager:
    def __init__(self):
        self.windows: list[window.Window] = []

    def update(self, dt: float):
        i = 0
        while i < len(self.windows):
            self.windows[i].update(dt)
            i += 1

        for w in self.windows:
            self._make_window_in_bound(w)

    def draw(self):
        i = len(self.windows) - 1
        while i >= 0:
            self.windows[i].draw()
            # Windows should not be destroyed at this point, therefore we don't need bound-checks here
            i -= 1

    def add_window(self, win: window.Window):
        # self.windows.append(window)
        self.windows.insert(0, win)
        win.manager = self

    def remove_window(self, win: window.Window):
        if win not in self.windows:
            return

        self.windows.remove(win)
        # TODO : maybe we shouldn't remove the reference ?
        win.manager = None

    def bring_on_top(self, win: window.Window):
        if win not in self.windows:
            return

        i = self.windows.index(win)
        del self.windows[i]
        self.windows.insert(0, win)

    def check_existence(self, window_type):
        """
        Check if a window of a specific type is open
        TODO : maybe letter we shouldn't rely on python type and instead have type identifiers on the windows ?
        """
        for win in self.windows:
            if isinstance(win, window_type):
                return True
        return False

    def _make_window_in_bound(self, win: window.Window):
        # TODO : make it so the window manager store a minimum and maximum position for the window
        if win.x < 0: win.set_position(0, win.y)
        elif win.x+win.width >= pyray.get_screen_width(): win.set_position(pyray.get_screen_width() - win.width - 1, win.y)

        if win.y < 0: win.set_position(win.x, 0)
        elif win.y + win.height >= pyray.get_screen_height(): win.set_position(win.x, pyray.get_screen_height() - win.height - 1)

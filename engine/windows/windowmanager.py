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

    def add_window(self, window: window.Window):
        # self.windows.append(window)
        self.windows.insert(0, window)
        window.manager = self

    def remove_window(self, window: window.Window):
        if window not in self.windows:
            return

        self.windows.remove(window)
        # TODO : maybe we shouldn't remove the reference ?
        window.manager = None

    def bring_on_top(self, window: window.Window):
        if window not in self.windows:
            return

        i = self.windows.index(window)
        del self.windows[i]
        self.windows.insert(0, window)

    def _make_window_in_bound(self, window: window.Window):
        # TODO : make it so the window manager store a minimum and maximum position for the window
        if window.x < 0: window.set_position(0, window.y)
        elif window.x+window.width >= pyray.get_screen_width(): window.set_position(pyray.get_screen_width() - window.width - 1, window.y)

        if window.y < 0: window.set_position(window.x, 0)
        elif window.y + window.height >= pyray.get_screen_height(): window.set_position(window.x, pyray.get_screen_height() - window.height - 1)

from editor import editorwindow


class WindowManager:
    def __init__(self):
        self.windows: list[editorwindow.EditorWindow] = []

    def update(self, dt: float):
        i = 0
        while i < len(self.windows):
            self.windows[i].update(dt)
            i += 1

    def draw(self):
        i = len(self.windows) - 1
        while i >= 0:
            self.windows[i].draw()
            # Windows should not be destroyed at this point, therefore we don't need bound-checks here
            i -= 1

    def add_window(self, window: editorwindow.EditorWindow):
        # self.windows.append(window)
        self.windows.insert(0, window)
        window.manager = self

    def remove_window(self, window: editorwindow.EditorWindow):
        if window not in self.windows:
            return

        self.windows.remove(window)
        # TODO : maybe we shouldn't remove the reference ?
        window.manager = None

    def bring_on_top(self, window: editorwindow.EditorWindow):
        if window not in self.windows:
            return

        i = self.windows.index(window)
        del self.windows[i]
        self.windows.insert(0, window)

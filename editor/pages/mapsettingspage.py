import pyray

from . import editorpage


class MapSettingsPage(editorpage.EditorPage):
    def __init__(self, editor):
        super().__init__("Map settings", editor)

    def update(self, dt: float):
        pass

    def draw(self):
        pyray.draw_text("Map settings lmao", 50, 50, 20, pyray.WHITE)

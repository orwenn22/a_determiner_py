import pyray

from engine import globals as g


class KeyboardCode:
    def __init__(self, code: str, callback):
        self.code = code
        self.current_index = 0
        self.executed = False
        self.callback = callback

    def update(self):
        if self.executed:
            return

        for k in range(pyray.KeyboardKey.KEY_A, pyray.KeyboardKey.KEY_Z + 1):
            if g.is_key_pressed(k):
                if ord(self.code[self.current_index]) == k:
                    self.current_index += 1
                else:
                    self.current_index = 0
                break

        if self.current_index == len(self.code):
            self.callback()
            self.executed = True

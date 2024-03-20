from engine.widget import label
from utils.valref import ValRef


class ValueLabel(label.Label):
    def __init__(self, x: int, y: int, placement: str,  value_reference: ValRef, font_size: int, color=(255, 255, 255, 255)):
        self.value_reference = value_reference
        self.saved_value = value_reference.get()
        super().__init__(x, y, placement, str(self.saved_value), font_size, color)

    def update(self):
        super().update()
        if self.saved_value != self.value_reference.get():
            self.saved_value = self.value_reference.get()
            self.set_text(str(self.saved_value))

    def draw(self):
        super().draw()

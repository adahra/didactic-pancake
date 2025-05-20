import pyxel

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = color + 1 if color < 15 else color - 1

    def draw(self, mouse_x, mouse_y):
        current_color = self.hover_color if self.is_hovered(mouse_x, mouse_y) else self.color
        pyxel.rect(self.x, self.y, self.width, self.height, current_color)
        text_width = len(self.text) * 4
        pyxel.text(
            self.x + (self.width - text_width) // 2,
            self.y + (self.height - 5) // 2,
            self.text,
            0 if current_color > 6 else 7
        )

    def is_hovered(self, mouse_x, mouse_y):
        return (
            self.x <= mouse_x <= self.x + self.width and
            self.y <= mouse_y <= self.y + self.height
        )
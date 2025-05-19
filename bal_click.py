import pyxel

class BalanceClicker:
    def __init__(self):
        pyxel.init(160, 120, title="Balance Clicker")
        self.light = 50
        self.dark = 50
        self.timer = 0

        pyxel.mouse(True)  # Enable mouse input

        pyxel.run(self.update, self.draw)

    def update(self):
        # Input mouse
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x = pyxel.mouse_x 
            y = pyxel.mouse_y

            if 20 <= x <= 70 and 90 <= y <= 110:
                self.light += 1
            elif 90 <= x <= 140 and 90 <= y <= 110:
                self.dark += 1

        # Otomatis saling mengimbangi
        self.timer += 1
        if self.timer > 10:  # setiap 0.5 detik
            diff = self.light - self.dark
            balance_shift = int(diff * 0.1)
            self.light -= balance_shift
            self.dark += balance_shift
            self.timer = 0

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, "Balance Clicker", pyxel.frame_count % 16)
        pyxel.text(20, 30, f"Light: {self.light}", 7)
        pyxel.text(90, 30, f"Dark:  {self.dark}", 13)

        # Tombol
        pyxel.rect(20, 90, 50, 20, 7)
        pyxel.text(35, 96, "LIGHT", 0)

        pyxel.rect(90, 90, 50, 20, 13)
        pyxel.text(105, 96, "DARK", 0)

        # Visualisasi bar keseimbangan
        total = self.light + self.dark
        if total > 0:
            light_ratio = int((self.light / total) * 100)
            pyxel.rect(20, 60, light_ratio, 10, 7)
            pyxel.rect(20 + light_ratio, 60, 100 - light_ratio, 10, 13)

BalanceClicker()
import pyxel
import random


class Particle:
    def __init__(self, x, y, col):
        self.x = x + random.randint(-2, 2)
        self.y = y + random.randint(-2, 2)
        self.vx = random.uniform(-0.5, 0.5)
        self.vy = random.uniform(-0.5, -1)
        self.col = col
        self.life = 20

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pyxel.pset(int(self.x), int(self.y), self.col)

class BalanceClicker:
    def __init__(self):
        pyxel.init(160, 120, title="Balance Clicker")
        
        self.light = 50
        self.dark = 50
        self.auto_light = 0
        self.auto_dark = 0
        self.auto_light_cost = 20
        self.auto_dark_cost = 20
        self.balance_timer = 0
        self.auto_timer = 0
        self.particles = []

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            x, y = pyxel.mouse_x, pyxel.mouse_y
            # Klik Light
            if 20 <= x <= 70 and 90 <= y <= 110:
                self.light += 1
                self.spawn_particles(35, 96, 7)
            # Klik Dark
            elif 90 <= x <= 140 and 90 <= y <= 110:
                self.dark += 1
                self.spawn_particles(105, 96, 13)
            # Beli auto light
            elif 10 <= x <= 70 and 10 <= y <= 20:
                if self.light >= self.auto_light_cost:
                    self.light -= self.auto_light_cost
                    self.auto_light += 1
                    self.auto_light_cost += 10
            # Beli auto dark
            elif 90 <= x <= 150 and 10 <= y <= 20:
                if self.dark >= self.auto_dark_cost:
                    self.dark -= self.auto_dark_cost
                    self.auto_dark += 1
                    self.auto_dark_cost += 10

        # Seimbangkan
        self.balance_timer += 1
        if self.balance_timer > 30:
            diff = self.light - self.dark
            balance_shift = int(diff * 0.1)
            self.light -= balance_shift
            self.dark += balance_shift
            self.balance_timer = 0

        # Auto click
        self.auto_timer += 1
        if self.auto_timer > 60:
            self.light += self.auto_light
            self.dark += self.auto_dark
            self.auto_timer = 0

        # Update partikel
        for p in self.particles:
            p.update()
        self.particles = [p for p in self.particles if p.life > 0]

    def spawn_particles(self, x, y, col):
        for _ in range(8):
            self.particles.append(Particle(x, y, col))

    def draw(self):
        pyxel.cls(0)

        # Teks judul
        pyxel.text(45, 0, "Balance Clicker", pyxel.frame_count % 16)

        # Tombol klik
        pyxel.rect(20, 90, 50, 20, 7)
        pyxel.text(35 + random.randint(-1, 1), 96 + random.randint(-1, 1), "LIGHT", 0)
        pyxel.rect(90, 90, 50, 20, 13)
        pyxel.text(105 + random.randint(-1, 1), 96 + random.randint(-1, 1), "DARK", 0)

        # Status
        pyxel.text(20, 30, f"Light: {self.light}", 7)
        pyxel.text(90, 30, f"Dark:  {self.dark}", 13)

        # Tombol upgrade
        pyxel.rect(10, 10, 60, 10, 5)
        pyxel.text(12, 11, f"+Auto {self.auto_light} ({self.auto_light_cost})", 0)
        pyxel.rect(90, 10, 60, 10, 1)
        pyxel.text(92, 11, f"+Auto {self.auto_dark} ({self.auto_dark_cost})", 0)

        # Bar keseimbangan animasi
        total = self.light + self.dark
        if total > 0:
            light_ratio = int((self.light / total) * 100)
            # Kedipkan warna bar
            flash_col_light = 7 if pyxel.frame_count % 20 < 10 else 6
            flash_col_dark = 13 if pyxel.frame_count % 20 < 10 else 1
            pyxel.rect(20, 60, light_ratio, 10, flash_col_light)
            pyxel.rect(20 + light_ratio, 60, 100 - light_ratio, 10, flash_col_dark)

        # Gambar partikel
        for p in self.particles:
            p.draw()

BalanceClicker()
# This code creates a simple balance clicker game using the Pyxel library.
# The player can click to gain light or dark points, and can purchase auto-clickers for each type.
# The game features a balance mechanic where the light and dark points will shift towards each other over time.
# The game also includes particle effects for a more engaging experience.
# The UI displays the current light and dark points, as well as the cost of the auto-clickers.
# The game is designed to be simple and easy to understand, making it suitable for beginners.
# The game features a simple UI displaying the current light and dark points, as well as the cost of the auto-clickers.
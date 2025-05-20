import pyxel

class IdleClicker:
    def __init__(self):
        # Inisialisasi game
        pyxel.init(200, 160, title="Balance Clicker ++")
        
        # Variabel game
        self.energy = 50
        self.max_energy = 100
        self.score = 0
        self.game_over = False
        
        # Variabel upgrade
        self.auto_clicker_level = 0
        self.energy_efficiency_level = 0
        self.click_power_level = 0
        
        self.auto_clicker_rate = 0
        self.energy_drain_rate = 0.2
        self.click_power = 5
        
        # Harga upgrade
        self.auto_clicker_cost = 10
        self.energy_efficiency_cost = 15
        self.click_power_cost = 20
        
        pyxel.mouse(True)  # Aktifkan mouse

        # Jalankan game
        pyxel.run(self.update, self.draw)
    
    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return

        # Klik mouse untuk menambah energi
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.energy += self.click_power
            self.score += 1
        
        # Auto-clicker (jika sudah di-upgrade)
        if self.auto_clicker_level > 0 and pyxel.frame_count % 30 == 0:
            self.energy += self.auto_clicker_level
        
        # Energi berkurang secara otomatis
        self.energy -= self.energy_drain_rate
        
        # Pastikan energi tidak melebihi maksimum
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        
        # Game over jika energi habis
        if self.energy <= 0:
            self.game_over = True
        
        # Beli upgrade jika tombol ditekan
        if pyxel.btnp(pyxel.KEY_1) and self.score >= self.auto_clicker_cost:
            self.buy_auto_clicker()
        if pyxel.btnp(pyxel.KEY_2) and self.score >= self.energy_efficiency_cost:
            self.buy_energy_efficiency()
        if pyxel.btnp(pyxel.KEY_3) and self.score >= self.click_power_cost:
            self.buy_click_power()
    
    def buy_auto_clicker(self):
        self.score -= self.auto_clicker_cost
        self.auto_clicker_level += 1
        self.auto_clicker_cost += 5  # Harga naik setelah dibeli
    
    def buy_energy_efficiency(self):
        self.score -= self.energy_efficiency_cost
        self.energy_efficiency_level += 1
        self.energy_drain_rate *= 0.9  # Pengurangan energi lebih lambat
        self.energy_efficiency_cost += 8
    
    def buy_click_power(self):
        self.score -= self.click_power_cost
        self.click_power_level += 1
        self.click_power += 2  # Klik lebih kuat
        self.click_power_cost += 10
    
    def reset_game(self):
        self.energy = 50
        self.score = 0
        self.game_over = False
        self.auto_clicker_level = 0
        self.energy_efficiency_level = 0
        self.click_power_level = 0
        self.auto_clicker_rate = 0
        self.energy_drain_rate = 0.2
        self.click_power = 5
        self.auto_clicker_cost = 10
        self.energy_efficiency_cost = 15
        self.click_power_cost = 20
    
    def draw(self):
        pyxel.cls(0)  # Background hitam
        
        # Gambar UI utama
        pyxel.text(5, 5, f"ENERGY: {int(self.energy)}/{self.max_energy}", 7)
        pyxel.text(5, 15, f"SCORE: {self.score}", 7)
        
        # Gambar balance bar
        bar_width = int((self.energy / self.max_energy) * 180)
        pyxel.rect(10, 30, bar_width, 10, 11)  # Bar hijau
        
        # Gambar upgrade shop
        pyxel.text(10, 50, "UPGRADES (Press 1/2/3):", 7)
        pyxel.text(15, 60, f"1. Auto-Clicker ({self.auto_clicker_cost} pts)", 9 if self.score >= self.auto_clicker_cost else 8)
        pyxel.text(15, 70, f"2. Energy Efficiency ({self.energy_efficiency_cost} pts)", 9 if self.score >= self.energy_efficiency_cost else 8)
        pyxel.text(15, 80, f"3. Click Power ({self.click_power_cost} pts)", 9 if self.score >= self.click_power_cost else 8)
        
        # Gambar status upgrade
        pyxel.text(10, 100, f"Auto-Clicker: Lv {self.auto_clicker_level}", 7)
        pyxel.text(10, 110, f"Energy Drain: {self.energy_drain_rate:.2f}/s", 7)
        pyxel.text(10, 120, f"Click Power: +{self.click_power}", 7)
        
        # Game over screen
        if self.game_over:
            pyxel.rect(50, 60, 100, 40, 1)
            pyxel.text(70, 70, "GAME OVER!", pyxel.frame_count % 16)
            pyxel.text(60, 80, "Press R to restart", 7)
            

# Jalankan game
IdleClicker()
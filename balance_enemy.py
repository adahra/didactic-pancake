import pyxel
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type, score):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.size = 10
        self.active = True
    
        if enemy_type == 0:
            self.color = 8  # Merah
            self.health = 3 + score // 15
            self.speed = 1.0 + score // 40 * 0.2
            self.score_value = 3
        elif enemy_type == 1:
            self.color = 10  # Hijau
            self.health = 2 + score // 20
            self.speed = 1.5 + score // 30 * 0.2
            self.score_value = 2
        else:
            self.color = 5  # Biru
            self.health = 8 + score // 10
            self.speed = 0.6 + score // 50 * 0.1
            self.score_value = 8

        self.max_health = self.health
        self.original_speed = self.speed
        self.slow_timer = 0

    def update(self):
        if self.slow_timer > 0:
            self.slow_timer -= 1
            self.speed = self.original_speed * 0.5
        else:
            self.speed = self.original_speed

        self.y += self.speed

        if self.type == 1:
            self.x += math.sin(pyxel.frame_count / 0.5) * 1.5  # Gerakan zig-zag

        if self.y > pyxel.height:
            self.active = False
    
    def draw(self):
        if self.type == 0:
            pyxel.rect(self.x, self.y, self.size, self.size, self.color)
        elif self.type == 1:
            pyxel.tri(self.x, self.y, 
                      self.x + self.size, 
                      self.y, 
                      self.y + self.size // 2, 
                      self.x - self.size, 
                      self.color)
        else:
            pyxel.hex(self.x - self.size // 2,
                      self.y + self.size // 2, 
                      self.size // 2, 
                      self.color)
            
        # Health bar
        if self.type == 1:
            health_width = int((self.health / self.max_health) * self.size)
            pyxel.rect(self.x, self.y - 5, health_width, 2, 11)  # Bar hijau

class IdleClicker:
    def __init__(self):
        pyxel.init(200, 200, title="Balance Clicker: Enemy Mode")
        
        # Variabel game
        self.energy = 50
        self.max_energy = 150
        self.score = 0
        self.game_over = False
        self.wave = 0
        
        self.upgrades = {
            "auto_clicker": {"level": 0, "cost": 10, "value": 1},
            "efficiency": {"level": 0, "cost": 15, "value": 0.2},
            "click_power": {"level": 0, "cost": 20, "value": 5},
            "slow_shot": {"level": 0, "cost": 25, "value": 3},
        }
        
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 30

        pyxel.mouse(True)  # Enable mouse input

        pyxel.run(self.update, self.draw)
    
    def spawn_enemy(self):
        x = random.randint(10, pyxel.width - 20)
        health = 2 + (self.score // 20)  # Musuh semakin kuat
        speed = 0.5 + (self.score // 50) * 0.2  # Musuh semakin cepat
        self.enemies.append(Enemy(x, -10, health, speed))
    
    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        
        # Spawn musuh
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            self.enemy_spawn_delay = max(30, 60 - (self.score // 10))  # Musuh semakin sering
        
        # Update musuh
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.active:
                self.enemies.remove(enemy)
                self.energy -= 5  # Energi berkurang jika musuh lolos
        
        # Klik mouse untuk menambah energi atau serang musuh
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mouse_x, mouse_y = pyxel.mouse_x, pyxel.mouse_y
            
            # Cek apakah klik mengenai musuh
            enemy_hit = False
            for enemy in self.enemies[:]:
                if (enemy.x <= mouse_x <= enemy.x + enemy.size and 
                    enemy.y <= mouse_y <= enemy.y + enemy.size):
                    enemy.health -= self.click_power
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += 3  # Bonus skor untuk mengalahkan musuh
                    enemy_hit = True
            
            # Jika tidak kena musuh, tambah energi
            if not enemy_hit:
                self.energy += self.click_power
                self.score += 1
        
        # Auto-clicker
        if self.auto_clicker_level > 0 and pyxel.frame_count % 30 == 0:
            self.energy += self.auto_clicker_level
        
        # Energi berkurang
        self.energy -= self.energy_drain_rate
        
        # Game over jika energi habis
        if self.energy <= 0:
            self.game_over = True
        
        # Beli upgrade
        if pyxel.btnp(pyxel.KEY_1) and self.score >= self.auto_clicker_cost:
            self.buy_auto_clicker()
        if pyxel.btnp(pyxel.KEY_2) and self.score >= self.energy_efficiency_cost:
            self.buy_energy_efficiency()
        if pyxel.btnp(pyxel.KEY_3) and self.score >= self.click_power_cost:
            self.buy_click_power()
    
    def buy_auto_clicker(self):
        self.score -= self.auto_clicker_cost
        self.auto_clicker_level += 1
        self.auto_clicker_cost += 5
    
    def buy_energy_efficiency(self):
        self.score -= self.energy_efficiency_cost
        self.energy_efficiency_level += 1
        self.energy_drain_rate *= 0.9
        self.energy_efficiency_cost += 8
    
    def buy_click_power(self):
        self.score -= self.click_power_cost
        self.click_power_level += 1
        self.click_power += 2
        self.click_power_cost += 10
    
    def reset_game(self):
        self.energy = 50
        self.score = 0
        self.game_over = False
        self.enemies = []
        self.enemy_spawn_timer = 0
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
        pyxel.cls(0)
        
        # UI utama
        pyxel.text(5, 5, f"ENERGY: {int(self.energy)}/{self.max_energy}", 7)
        pyxel.text(5, 15, f"SCORE: {self.score}", 7)
        
        # Balance bar
        bar_width = int((self.energy / self.max_energy) * 180)
        pyxel.rect(10, 30, bar_width, 10, 11)
        
        # Upgrade shop
        pyxel.text(10, 50, "UPGRADES (Press 1/2/3):", 7)
        pyxel.text(15, 60, f"1. Auto-Clicker ({self.auto_clicker_cost} pts)", 9 if self.score >= self.auto_clicker_cost else 8)
        pyxel.text(15, 70, f"2. Energy Efficiency ({self.energy_efficiency_cost} pts)", 9 if self.score >= self.energy_efficiency_cost else 8)
        pyxel.text(15, 80, f"3. Click Power ({self.click_power_cost} pts)", 9 if self.score >= self.click_power_cost else 8)
        
        # Status upgrade
        pyxel.text(10, 100, f"Auto-Clicker: Lv {self.auto_clicker_level}", 7)
        pyxel.text(10, 110, f"Energy Drain: {self.energy_drain_rate:.2f}/s", 7)
        pyxel.text(10, 120, f"Click Power: +{self.click_power}", 7)
        
        # Gambar musuh
        for enemy in self.enemies:
            enemy.draw()
        
        # Game over
        if self.game_over:
            pyxel.rect(50, 70, 100, 40, 1)
            pyxel.text(70, 80, "GAME OVER!", pyxel.frame_count % 16)
            pyxel.text(60, 90, "Press R to restart", 7)

IdleClicker()
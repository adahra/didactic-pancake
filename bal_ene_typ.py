import pyxel
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type, level):
        self.x = x
        self.y = y
        self.type = enemy_type  # 0: Normal, 1: Fast, 2: Tank, 3: Boss
        self.size = 10
        self.active = True
        self.level = level
        
        # Properti berdasarkan jenis musuh dan level
        if enemy_type == 0:  # Normal
            self.color = 8
            self.health = 3 + level
            self.speed = 1.0 + level * 0.1
            self.score_value = 3
            self.damage = 5
        elif enemy_type == 1:  # Fast
            self.color = 10
            self.health = 1 + level // 2
            self.speed = 2.5 + level * 0.15
            self.score_value = 5
            self.damage = 3
        elif enemy_type == 2:  # Tank
            self.color = 5
            self.health = 8 + level * 2
            self.speed = 0.6 + level * 0.05
            self.score_value = 8
            self.damage = 10
        else:  # Boss (type 3)
            self.color = 7
            self.size = 16
            self.health = 20 + level * 5
            self.speed = 0.4
            self.score_value = 20
            self.damage = 15
            
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
        
        # Gerakan khusus
        if self.type == 1:  # Fast (zig-zag)
            self.x += math.sin(pyxel.frame_count * 0.1) * 1.5
        elif self.type == 3:  # Boss (bergerak horizontal)
            self.x += math.sin(pyxel.frame_count * 0.05) * 2
        
        if self.y > pyxel.height:
            self.active = False
    
    def draw(self):
        if self.type == 0:  # Normal
            pyxel.rect(self.x, self.y, self.size, self.size, self.color)
        elif self.type == 1:  # Fast
            pyxel.tri(self.x, self.y, 
                     self.x + self.size, self.y,
                     self.x + self.size//2, self.y - self.size, 
                     self.color)
        elif self.type == 2:  # Tank
            pyxel.rect(self.x, self.y, self.size, self.size, self.color)
            pyxel.line(self.x, self.y, self.x + self.size, self.y + self.size, self.color)
            pyxel.line(self.x + self.size, self.y, self.x, self.y + self.size, self.color)
        else:  # Boss
            pyxel.rectb(self.x, self.y, self.size, self.size, self.color)
            pyxel.circ(self.x + self.size//2, self.y + self.size//2, self.size//3, self.color)
        
        # Health bar
        if self.type != 1 or self.type == 3:  # Semua kecuali Fast, Boss selalu ada
            health_width = int((self.health/self.max_health) * self.size)
            pyxel.rect(self.x, self.y - 5, health_width, 2, 11)

class IdleClicker:
    def __init__(self):
        pyxel.init(200, 220, title="Balance Clicker: Level System")
        pyxel.mouse(True)
        
        # Game state
        self.energy = 50
        self.max_energy = 150
        self.score = 0
        self.level = 1
        self.level_progress = 0
        self.level_up_requirement = 30
        self.game_over = False
        
        # Upgrade system
        self.upgrades = {
            "auto_clicker": {"level": 0, "cost": 10, "value": 1},
            "efficiency": {"level": 0, "cost": 15, "value": 0.2},
            "click_power": {"level": 0, "cost": 20, "value": 5},
            "slow_shot": {"level": 0, "cost": 25, "value": 3}
        }
        
        # Enemy system
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 45
        self.boss_spawned = False
        
        pyxel.run(self.update, self.draw)
    
    def spawn_enemy(self):
        # Spawn boss setiap 5 level
        if self.level % 5 == 0 and not self.boss_spawned and len(self.enemies) == 0:
            enemy_type = 3  # Boss
            self.boss_spawned = True
        else:
            weights = [70 - self.level, 20 + self.level//2, 10 + self.level//3]
            enemy_type = random.choices([0, 1, 2], weights=weights)[0]
        
        x = random.randint(20, pyxel.width - 30)
        self.enemies.append(Enemy(x, -20, enemy_type, self.level))
    
    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset_game()
            return
        
        # Level progression
        if self.score >= self.level_up_requirement:
            self.level_up()
        
        # Enemy spawning
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.spawn_enemy()
            self.enemy_spawn_timer = 0
            self.enemy_spawn_delay = max(20, 50 - self.level)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.active:
                self.enemies.remove(enemy)
                self.energy -= enemy.damage
                if enemy.type == 3:  # Jika boss lolos
                    self.energy -= 20
        
        # Mouse click
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            hit = False
            
            for enemy in self.enemies[:]:
                if (enemy.x <= mx <= enemy.x + enemy.size and 
                    enemy.y <= my <= enemy.y + enemy.size):
                    enemy.health -= self.upgrades["click_power"]["value"]
                    if self.upgrades["slow_shot"]["level"] > 0:
                        enemy.slow_timer = 20
                    
                    if enemy.health <= 0:
                        self.enemies.remove(enemy)
                        self.score += enemy.score_value
                        self.energy += 2
                        if enemy.type == 3:  # Kalahkan boss
                            self.score += 50
                            self.energy += 10
                            self.boss_spawned = False
                    hit = True
            
            if not hit:
                self.energy += self.upgrades["click_power"]["value"]
                self.score += 1
        
        # Auto-clicker
        if self.upgrades["auto_clicker"]["level"] > 0 and pyxel.frame_count % 30 == 0:
            self.energy += self.upgrades["auto_clicker"]["level"]
        
        # Energy drain
        self.energy -= self.upgrades["efficiency"]["value"]
        
        # Game over check
        if self.energy <= 0:
            self.game_over = True
        
        # Upgrade keys
        keys = [pyxel.KEY_1, pyxel.KEY_2, pyxel.KEY_3, pyxel.KEY_4]
        for i, upgrade in enumerate(self.upgrades.keys()):
            if pyxel.btnp(keys[i]) and self.score >= self.upgrades[upgrade]["cost"]:
                self.buy_upgrade(upgrade)
    
    def level_up(self):
        self.level += 1
        self.level_up_requirement += self.level * 15
        self.max_energy += 20
        self.energy = min(self.energy + 30, self.max_energy)
        
        # Reset progress
        self.level_progress = 0
        
        # Bersihkan musuh saat naik level
        self.enemies.clear()
        self.boss_spawned = False
    
    def buy_upgrade(self, upgrade):
        self.score -= self.upgrades[upgrade]["cost"]
        self.upgrades[upgrade]["level"] += 1
        self.upgrades[upgrade]["cost"] += int(self.upgrades[upgrade]["cost"] * 0.5)
        
        if upgrade == "efficiency":
            self.upgrades[upgrade]["value"] *= 0.9
    
    def reset_game(self):
        self.energy = 50
        self.max_energy = 150
        self.score = 0
        self.level = 1
        self.level_progress = 0
        self.level_up_requirement = 30
        self.game_over = False
        self.enemies = []
        self.boss_spawned = False
        
        for upgrade in self.upgrades.values():
            upgrade["level"] = 0
            if "original_cost" in upgrade:
                upgrade["cost"] = upgrade["original_cost"]
    
    def draw(self):
        pyxel.cls(0)
        
        # UI Top
        pyxel.text(5, 5, f"ENERGY: {int(self.energy)}/{self.max_energy}", 7)
        pyxel.text(5, 15, f"SCORE: {self.score}", 7)
        pyxel.text(5, 25, f"LEVEL: {self.level}", 7)
        
        # Progress bar
        progress = min(1.0, self.score / self.level_up_requirement)
        pyxel.rect(5, 35, int(190 * progress), 5, 9)
        pyxel.rectb(5, 35, 190, 5, 13)
        pyxel.text(80, 35, f"NEXT LEVEL: {self.level_up_requirement}", 7)
        
        # Energy bar
        energy_ratio = self.energy / self.max_energy
        pyxel.rect(5, 45, int(190 * energy_ratio), 5, 11)
        pyxel.rectb(5, 45, 190, 5, 13)
        
        # Upgrade panel
        pyxel.text(5, 55, "UPGRADES (1-4):", 7)
        for i, (name, data) in enumerate(self.upgrades.items()):
            color = 9 if self.score >= data["cost"] else 8
            pyxel.text(10, 65 + i*10, 
                      f"{i+1}. {name.replace('_',' ').title()} (Lv:{data['level']}) - {data['cost']}pts",
                      color)
        
        # Enemies
        for enemy in self.enemies:
            enemy.draw()
        
        # Game over
        if self.game_over:
            pyxel.rect(50, 80, 100, 50, 1)
            pyxel.text(65, 90, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(60, 100, f"Reached Level: {self.level}", 7)
            pyxel.text(55, 110, "Press R to restart", 7)

IdleClicker()
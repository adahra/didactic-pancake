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

class IdleClicker:
    def __init__(self):
        pyxel.init(200, 240, title="Balance Clicker: Mouse Control")
        pyxel.mouse(True)
        
        # Game state
        self.energy = 50
        self.max_energy = 150
        self.score = 0
        self.level = 1
        self.level_progress = 0
        self.level_up_requirement = 30
        self.game_over = False
        self.show_upgrades = False
        
        # Upgrade system
        self.upgrades = {
            "Auto-Clicker": {"level": 0, "cost": 10, "value": 1},
            "Efficiency": {"level": 0, "cost": 15, "value": 0.2},
            "Click Power": {"level": 0, "cost": 20, "value": 5},
            "Slow Shot": {"level": 0, "cost": 25, "value": 3}
        }
        
        # Enemy system
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 45
        self.boss_spawned = False
        
        # Buttons
        self.upgrade_button = Button(10, 180, 180, 15, "UPGRADES", 5)
        self.upgrade_buttons = [
            Button(10, 60 + i*25, 180, 20, 
                  f"{name} (Lv:{data['level']}) - {data['cost']}pts", 
                  9 if self.score >= data["cost"] else 8)
            for i, (name, data) in enumerate(self.upgrades.items())
        ]
        self.close_button = Button(160, 60, 30, 15, "X", 8)
        
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
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mx, my = pyxel.mouse_x, pyxel.mouse_y
                if 70 <= mx <= 130 and 110 <= my <= 130:  # Tombol restart
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
        
        # Mouse click handling
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            
            # Cek klik upgrade button
            if self.upgrade_button.is_hovered(mx, my):
                self.show_upgrades = not self.show_upgrades
            
            # Cek klik close button
            elif self.show_upgrades and self.close_button.is_hovered(mx, my):
                self.show_upgrades = False
            
            # Cek klik tombol upgrade
            elif self.show_upgrades:
                for i, button in enumerate(self.upgrade_buttons):
                    upgrade_name = list(self.upgrades.keys())[i]
                    if button.is_hovered(mx, my) and self.score >= self.upgrades[upgrade_name]["cost"]:
                        self.buy_upgrade(upgrade_name)
                        # Update button text
                        button.text = f"{upgrade_name} (Lv:{self.upgrades[upgrade_name]['level']}) - {self.upgrades[upgrade_name]['cost']}pts"
            
            # Cek klik musuh atau background
            else:
                hit_enemy = False
                for enemy in self.enemies[:]:
                    if (enemy.x <= mx <= enemy.x + enemy.size and 
                        enemy.y <= my <= enemy.y + enemy.size):
                        enemy.health -= self.upgrades["Click Power"]["value"]
                        if self.upgrades["Slow Shot"]["level"] > 0:
                            enemy.slow_timer = 20
                        
                        if enemy.health <= 0:
                            self.enemies.remove(enemy)
                            self.score += enemy.score_value
                            self.energy += 2
                            if enemy.type == 3:  # Kalahkan boss
                                self.score += 50
                                self.energy += 10
                                self.boss_spawned = False
                        hit_enemy = True
                
                if not hit_enemy:
                    self.energy += self.upgrades["Click Power"]["value"]
                    self.score += 1
        
        # Auto-clicker
        if self.upgrades["Auto-Clicker"]["level"] > 0 and pyxel.frame_count % 30 == 0:
            self.energy += self.upgrades["Auto-Clicker"]["level"]
        
        # Energy drain
        self.energy -= self.upgrades["Efficiency"]["value"]
        
        # Game over check
        if self.energy <= 0:
            self.game_over = True
    
    def level_up(self):
        self.level += 1
        self.level_up_requirement += self.level * 15
        self.max_energy += 20
        self.energy = min(self.energy + 30, self.max_energy)
        self.level_progress = 0
        self.enemies.clear()
        self.boss_spawned = False
    
    def buy_upgrade(self, upgrade_name):
        self.score -= self.upgrades[upgrade_name]["cost"]
        self.upgrades[upgrade_name]["level"] += 1
        self.upgrades[upgrade_name]["cost"] += int(self.upgrades[upgrade_name]["cost"] * 0.5)
        
        if upgrade_name == "Efficiency":
            self.upgrades[upgrade_name]["value"] *= 0.9
    
    def reset_game(self):
        self.energy = 50
        self.max_energy = 150
        self.score = 0
        self.level = 1
        self.level_progress = 0
        self.level_up_requirement = 30
        self.game_over = False
        self.show_upgrades = False
        self.enemies = []
        self.boss_spawned = False
        
        for upgrade in self.upgrades.values():
            upgrade["level"] = 0
            if "original_cost" in upgrade:
                upgrade["cost"] = upgrade["original_cost"]
        
        # Reset upgrade buttons text
        for i, (name, data) in enumerate(self.upgrades.items()):
            self.upgrade_buttons[i].text = f"{name} (Lv:{data['level']}) - {data['cost']}pts"
    
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
        
        # Draw upgrade button
        self.upgrade_button.draw(pyxel.mouse_x, pyxel.mouse_y)
        
        # Draw upgrade panel if shown
        if self.show_upgrades:
            pyxel.rect(5, 55, 190, 120, 1)
            pyxel.rectb(5, 55, 190, 120, 3)
            pyxel.text(75, 60, "UPGRADE SHOP", 7)
            self.close_button.draw(pyxel.mouse_x, pyxel.mouse_y)
            
            for button in self.upgrade_buttons:
                button.draw(pyxel.mouse_x, pyxel.mouse_y)
        
        # Enemies
        for enemy in self.enemies:
            enemy.draw()
        
        # Game over screen
        if self.game_over:
            pyxel.rect(50, 80, 100, 60, 1)
            pyxel.rectb(50, 80, 100, 60, 3)
            pyxel.text(65, 90, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(60, 100, f"Level: {self.level}", 7)
            pyxel.text(60, 110, f"Score: {self.score}", 7)
            
            # Restart button
            restart_color = 11 if (70 <= pyxel.mouse_x <= 130 and 110 <= pyxel.mouse_y <= 130) else 8
            pyxel.rect(70, 120, 60, 15, restart_color)
            pyxel.text(85, 123, "RESTART", 0)

IdleClicker()
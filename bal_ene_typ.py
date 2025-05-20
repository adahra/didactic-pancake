import pyxel
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type, level):
        self.x = x
        self.y = y
        self.type = enemy_type  # 0: Normal, 1: Fast, 2: Tank, 3: Boss
        self.size = 8
        self.active = True
        self.level = level
        self.animation_frame = 0
        
        # Properti berdasarkan jenis musuh dan level
        if enemy_type == 0:  # Normal
            self.color = 8
            self.health = 3 + level
            self.speed = 1.0 + level * 0.1
            self.score_value = 3
            self.damage = 5
            self.sprite_u = 0
            self.sprite_v = 0
        elif enemy_type == 1:  # Fast
            self.color = 10
            self.health = 1 + level // 2
            self.speed = 2.5 + level * 0.15
            self.score_value = 5
            self.damage = 3
            self.sprite_u = 8
            self.sprite_v = 0
        elif enemy_type == 2:  # Tank
            self.color = 5
            self.health = 8 + level * 2
            self.speed = 0.6 + level * 0.05
            self.score_value = 8
            self.damage = 10
            self.sprite_u = 16
            self.sprite_v = 0
        else:  # Boss (type 3)
            self.color = 7
            self.size = 16
            self.health = 20 + level * 5
            self.speed = 0.4
            self.score_value = 20
            self.damage = 15
            self.sprite_u = 0
            self.sprite_v = 16
            
        self.max_health = self.health
        self.original_speed = self.speed
        self.slow_timer = 0
    
    def update(self):
        self.animation_frame = (pyxel.frame_count // 5) % 2
        
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
        # Gambar sprite musuh
        if self.type == 3:  # Boss
            pyxel.blt(
                self.x, self.y, 0,
                self.sprite_u + (16 if self.animation_frame else 0),
                self.sprite_v,
                16, 16,
                0
            )
        else:
            pyxel.blt(
                self.x, self.y, 0,
                self.sprite_u + (8 if self.animation_frame else 0),
                self.sprite_v,
                8, 8,
                0
            )
        
        # Health bar
        if self.type != 1 or self.type == 3:  # Semua kecuali Fast, Boss selalu ada
            health_width = int((self.health/self.max_health) * self.size)
            pyxel.rect(self.x, self.y - 5, health_width, 2, 11)

class Button:
    def __init__(self, x, y, width, height, text, color, sound_channel=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = color + 1 if color < 15 else color - 1
        self.sound_channel = sound_channel
    
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
    
    def play_sound(self):
        if self.sound_channel == 0:
            pyxel.play(0, 0)  # Sound pendek untuk tombol
        else:
            pyxel.play(1, 1)  # Sound berbeda untuk upgrade

class Player:
    def __init__(self):
        self.x = pyxel.width // 2
        self.y = pyxel.height - 20
        self.click_effect = 0
    
    def draw(self):
        # Gambar cursor custom
        mx, my = pyxel.mouse_x, pyxel.mouse_y
        pyxel.blt(
            mx - 4, my - 4, 0,
            24, 0,
            8, 8,
            0
        )
        
        # Efek klik
        if self.click_effect > 0:
            pyxel.circ(mx, my, self.click_effect, 10)
            self.click_effect -= 0.5
    
    def show_click(self):
        self.click_effect = 5

class IdleClicker:
    def __init__(self):
        pyxel.init(200, 240, title="Balance Clicker: Pixel Edition")
        pyxel.mouse(False)  # Sembunyikan cursor default
        
        # Load assets
        self.load_assets()
        
        # Game state
        self.player = Player()
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
                  9 if self.score >= data["cost"] else 8, 1)
            for i, (name, data) in enumerate(self.upgrades.items())
        ]
        self.close_button = Button(160, 60, 30, 15, "X", 8)
        self.restart_button = Button(70, 120, 60, 15, "RESTART", 11)
        
        pyxel.run(self.update, self.draw)
    
    def load_assets(self):
        # Buat image bank dan muat sprite
        pyxel.image(0).set(
            # Enemy sprites (8x8)
            # Normal (2 frame animasi)
            0, 0, [
                "00777000",
                "07000700",
                "70000070",
                "77777770",
                "70000070",
                "70000070",
                "07000700",
                "00777000"
            ] + [
                "00777000",
                "07000700",
                "70000070",
                "70000070",
                "77777770",
                "70000070",
                "07000700",
                "00777000"
            ],
            # Fast enemy (2 frame)
            8, 0, [
                "00077000",
                "00700700",
                "07000070",
                "70000007",
                "70000007",
                "07000070",
                "00700700",
                "00077000"
            ] + [
                "00077000",
                "00700700",
                "07000070",
                "70000007",
                "70000007",
                "07000070",
                "00700700",
                "00077000"
            ],
            # Tank enemy (2 frame)
            16, 0, [
                "07777770",
                "70000007",
                "7cccccc7",
                "7cccccc7",
                "7cccccc7",
                "7cccccc7",
                "70000007",
                "07777770"
            ] + [
                "07777770",
                "70000007",
                "7cccccc7",
                "7cccccc7",
                "7cccccc7",
                "7cccccc7",
                "70000007",
                "07777770"
            ],
            # Cursor (8x8)
            24, 0, [
                "00001000",
                "00010100",
                "00111100",
                "01111110",
                "00111100",
                "00010100",
                "00001000",
                "00000000"
            ],
            # Boss sprite (16x16)
            0, 16, [
                "0000007777770000",
                "0000777777777700",
                "0007777777777770",
                "0077777777777777",
                "0777777777777777",
                "0777777777777777",
                "7777777777777777",
                "7777777777777777",
                "7777777777777777",
                "7777777777777777",
                "0777777777777777",
                "0777777777777777",
                "0077777777777777",
                "0007777777777770",
                "0000777777777700",
                "0000007777770000"
            ] + [
                "0000007777770000",
                "0000777777777700",
                "0007777777777770",
                "0077777777777777",
                "0777777777777777",
                "0777777777777777",
                "7777777777777777",
                "7777777777777777",
                "7777777777777777",
                "7777777777777777",
                "0777777777777777",
                "0777777777777777",
                "0077777777777777",
                "0007777777777770",
                "0000777777777700",
                "0000007777770000"
            ]
        )
        
        # Sound effects
        pyxel.sound(0).set(
            "c2e2g2c3", "s", "6", "nnnn", 32
        )
        pyxel.sound(1).set(
            "e3b2g2", "s", "6", "nnn", 32
        )
        pyxel.sound(2).set(
            "a3g3f3e3", "t", "7", "nnnn", 16
        )
        pyxel.sound(3).set(
            "c3c3c3", "n", "6", "fff", 8
        )
    
    def spawn_enemy(self):
        # Spawn boss setiap 5 level
        if self.level % 5 == 0 and not self.boss_spawned and len(self.enemies) == 0:
            enemy_type = 3  # Boss
            self.boss_spawned = True
            pyxel.play(3, 3)  # Sound spawn boss
        else:
            weights = [70 - self.level, 20 + self.level//2, 10 + self.level//3]
            enemy_type = random.choices([0, 1, 2], weights=weights)[0]
        
        x = random.randint(20, pyxel.width - 30)
        self.enemies.append(Enemy(x, -20, enemy_type, self.level))
    
    def update(self):
        if self.game_over:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mx, my = pyxel.mouse_x, pyxel.mouse_y
                if self.restart_button.is_hovered(mx, my):
                    self.restart_button.play_sound()
                    pyxel.play(2, 2)  # Sound restart
                    pyxel.flush()
                    self.reset_game()
            return
        
        # Level progression
        if self.score >= self.level_up_requirement:
            self.level_up()
            pyxel.play(2, 2)  # Sound level up
        
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
                pyxel.play(0, 0)  # Sound musuh lolos
        
        # Mouse click handling
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.player.show_click()
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            
            # Cek klik upgrade button
            if self.upgrade_button.is_hovered(mx, my):
                self.upgrade_button.play_sound()
                self.show_upgrades = not self.show_upgrades
            
            # Cek klik close button
            elif self.show_upgrades and self.close_button.is_hovered(mx, my):
                self.close_button.play_sound()
                self.show_upgrades = False
            
            # Cek klik tombol upgrade
            elif self.show_upgrades:
                for i, button in enumerate(self.upgrade_buttons):
                    upgrade_name = list(self.upgrades.keys())[i]
                    if button.is_hovered(mx, my) and self.score >= self.upgrades[upgrade_name]["cost"]:
                        button.play_sound()
                        self.buy_upgrade(upgrade_name)
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
                            pyxel.play(1, 1)  # Sound musuh mati
                            self.enemies.remove(enemy)
                            self.score += enemy.score_value
                            self.energy += 2
                            if enemy.type == 3:  # Kalahkan boss
                                self.score += 50
                                self.energy += 10
                                self.boss_spawned = False
                                pyxel.play(2, 2)  # Sound kalahkan boss
                        else:
                            pyxel.play(0, 0)  # Sound hit musuh
                        hit_enemy = True
                
                if not hit_enemy:
                    pyxel.play(0, 0)  # Sound klik biasa
                    self.energy += self.upgrades["Click Power"]["value"]
                    self.score += 1
        
        # Auto-clicker
        if self.upgrades["Auto-Clicker"]["level"] > 0 and pyxel.frame_count % 30 == 0:
            self.energy += self.upgrades["Auto-Clicker"]["level"]
        
        # Energy drain
        self.energy -= self.upgrades["Efficiency"]["value"]
        
        # Game over check
        if self.energy <= 0:
            pyxel.play(3, 3)  # Sound game over
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
        
        # Gambar background
        for y in range(0, pyxel.height, 8):
            for x in range(0, pyxel.width, 8):
                pyxel.rect(x, y, 8, 8, 1 if (x//8 + y//8) % 2 == 0 else 0)
        
        # UI Top
        pyxel.rect(0, 0, pyxel.width, 50, 1)
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
        
        # Player cursor
        self.player.draw()
        
        # Game over screen
        if self.game_over:
            pyxel.rect(50, 80, 100, 60, 1)
            pyxel.rectb(50, 80, 100, 60, 3)
            pyxel.text(65, 90, "GAME OVER", pyxel.frame_count % 16)
            pyxel.text(60, 100, f"Level: {self.level}", 7)
            pyxel.text(60, 110, f"Score: {self.score}", 7)
            
            self.restart_button.draw(pyxel.mouse_x, pyxel.mouse_y)

IdleClicker()
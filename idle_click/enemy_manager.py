import random
import pyxel
from enemy import Enemy

class EnemyManager:
    def __init__(self):
        self.enemies = []
        self.enemy_spawn_timer = 0
        self.enemy_spawn_delay = 45
        self.boss_spawned = False

    def spawn_enemy(self, level):
        if level % 5 == 0 and not self.boss_spawned and len(self.enemies) == 0:
            enemy_type = 3
            self.boss_spawned = True
        else:
            weights = [70 - level, 20 + level//2, 10 + level//3]
            enemy_type = random.choices([0, 1, 2], weights=weights)[0]
        x = random.randint(20, pyxel.width - 30)
        self.enemies.append(Enemy(x, -20, enemy_type, level))

    def update_enemies(self):
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.active:
                self.enemies.remove(enemy)

    def clear(self):
        self.enemies.clear()
        self.boss_spawned = False
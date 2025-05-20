import pyxel
import math

class Enemy:
    def __init__(self, x, y, enemy_type, level):
        self.x = x
        self.y = y
        self.type = enemy_type
        self.size = 10
        self.active = True
        self.level = level

        if enemy_type == 0:
            self.color = 8
            self.health = 3 + level
            self.speed = 1.0 + level * 0.1
            self.score_value = 3
            self.damage = 5
        elif enemy_type == 1:
            self.color = 10
            self.health = 1 + level // 2
            self.speed = 2.5 + level * 0.15
            self.score_value = 5
            self.damage = 3
        elif enemy_type == 2:
            self.color = 5
            self.health = 8 + level * 2
            self.speed = 0.6 + level * 0.05
            self.score_value = 8
            self.damage = 10
        else:
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

        if self.type == 1:
            self.x += math.sin(pyxel.frame_count * 0.1) * 1.5
        elif self.type == 3:
            self.x += math.sin(pyxel.frame_count * 0.05) * 2

        if self.y > pyxel.height:
            self.active = False

    def draw(self):
        if self.type == 0:
            pyxel.rect(self.x, self.y, self.size, self.size, self.color)
        elif self.type == 1:
            pyxel.tri(self.x, self.y,
                      self.x + self.size, self.y,
                      self.x + self.size//2, self.y - self.size,
                      self.color)
        elif self.type == 2:
            pyxel.rect(self.x, self.y, self.size, self.size, self.color)
            pyxel.line(self.x, self.y, self.x + self.size, self.y + self.size, self.color)
            pyxel.line(self.x + self.size, self.y, self.x, self.y + self.size, self.color)
        else:
            pyxel.rectb(self.x, self.y, self.size, self.size, self.color)
            pyxel.circ(self.x + self.size//2, self.y + self.size//2, self.size//3, self.color)

        if self.type != 1 or self.type == 3:
            health_width = int((self.health/self.max_health) * self.size)
            pyxel.rect(self.x, self.y - 5, health_width, 2, 11)
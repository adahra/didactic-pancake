import pyxel
from upgrade_manager import UpgradeManager
from enemy_manager import EnemyManager
from ui_manager import UIManager


class IdleClicker:
    def __init__(self):
        pyxel.init(200, 240, title="Balance Clicker: Mouse Control")
        pyxel.mouse(True)

        self.init_sounds()

        self.energy = 50
        self.max_energy = 150
        self.score = 0
        self.level = 1
        self.level_up_requirement = 30
        self.game_over = False
        self.show_upgrades = False

        self.upgrade_manager = UpgradeManager()
        self.enemy_manager = EnemyManager()
        self.ui_manager = UIManager(self.upgrade_manager)

        self.play_music(True, True, True)

        pyxel.run(self.update, self.draw)


    def play_music(self, ch0, ch1, ch2):
        if ch0:
            pyxel.play(0, [0, 1], loop=True)
        else:
            pyxel.stop(0)

        if ch1:
            pyxel.play(1, [2, 3], loop=True)
        else:
            pyxel.stop(1)

        if ch2:
            pyxel.play(2, 4, loop=True)
        else:
            pyxel.stop(2)


    def init_sounds(self):
        pyxel.sounds[0].set(
            "e2e2c2g1 g1g1c2e2 d2d2d2g2 g2g2rr c2c2a1e1 e1e1a1c2 b1b1b1e2 e2e2rr",
            "p",
            "6",
            "vffn fnff vffs vfnn",
            25,
        )
        pyxel.sounds[1].set(
            "r a1b1c2 b1b1c2d2 g2g2g2g2 c2c2d2e2 f2f2f2e2 f2e2d2c2 d2d2d2d2 g2g2r r ",
            "s",
            "6",
            "nnff vfff vvvv vfff svff vfff vvvv svnn",
            25,
        )
        pyxel.sounds[2].set(
            "c1g1c1g1 c1g1c1g1 b0g1b0g1 b0g1b0g1 a0e1a0e1 a0e1a0e1 g0d1g0d1 g0d1g0d1",
            "t",
            "7",
            "n",
            25,
        )
        pyxel.sounds[3].set(
            "f0c1f0c1 g0d1g0d1 c1g1c1g1 a0e1a0e1 f0c1f0c1 f0c1f0c1 g0d1g0d1 g0d1g0d1",
            "t",
            "7",
            "n",
            25,
        )
        pyxel.sounds[4].set(
            "f0ra4r f0ra4r f0ra4r f0f0a4r", "n", "6622 6622 6622 6422", "f", 25
        )


    def update(self):
        if self.game_over:
            self.handle_game_over_input()
            return

        self.handle_level_progression()
        self.handle_enemy_spawning()
        self.enemy_manager.update_enemies()
        self.handle_mouse_clicks()
        self.handle_auto_clicker()
        self.handle_energy_drain()
        self.check_game_over()

    def handle_game_over_input(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if 70 <= mx <= 130 and 110 <= my <= 130:
                # pyxel.play(0, 0)
                self.reset_game()

    def handle_level_progression(self):
        if self.score >= self.level_up_requirement:
            self.level += 1
            self.level_up_requirement += self.level * 15
            self.max_energy += 20
            self.energy = min(self.energy + 30, self.max_energy)
            self.enemy_manager.clear()

    def handle_enemy_spawning(self):
        self.enemy_manager.enemy_spawn_timer += 1
        if self.enemy_manager.enemy_spawn_timer >= self.enemy_manager.enemy_spawn_delay:
            self.enemy_manager.spawn_enemy(self.level)
            self.enemy_manager.enemy_spawn_timer = 0
            self.enemy_manager.enemy_spawn_delay = max(20, 50 - self.level)

    def handle_mouse_clicks(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            if self.ui_manager.upgrade_button.is_hovered(mx, my):
                # self.ui_manager.upgrade_button.play_sound()
                self.show_upgrades = not self.show_upgrades
            elif self.show_upgrades and self.ui_manager.close_button.is_hovered(mx, my):
                # self.ui_manager.close_button.play_sound()
                self.show_upgrades = False
            elif self.show_upgrades:
                for i, button in enumerate(self.ui_manager.upgrade_buttons):
                    upgrade_name = list(
                        self.upgrade_manager.upgrades.keys())[i]
                    if button.is_hovered(mx, my) and self.upgrade_manager.can_buy(upgrade_name, self.energy):
                        # button.play_sound()
                        self.energy -= self.upgrade_manager.upgrades[upgrade_name]["cost"]
                        self.upgrade_manager.buy(upgrade_name)
                        self.ui_manager.update_upgrade_buttons(
                            self.upgrade_manager.upgrades, self.energy)
            else:
                hit_enemy = False
                for enemy in self.enemy_manager.enemies[:]:
                    if (enemy.x <= mx <= enemy.x + enemy.size and
                            enemy.y <= my <= enemy.y + enemy.size):
                        enemy.health -= self.upgrade_manager.upgrades["Click Power"]["value"]
                        if self.upgrade_manager.upgrades["Slow Shot"]["level"] > 0:
                            enemy.slow_timer = 20
                        if enemy.health <= 0:
                            self.enemy_manager.enemies.remove(enemy)
                            self.score += enemy.score_value
                            self.energy += 2
                            self.energy = min(self.energy, self.max_energy)
                            if enemy.type == 3:
                                self.score += 50
                                self.energy += 10
                                self.energy = min(self.energy, self.max_energy)
                                self.enemy_manager.boss_spawned = False
                        hit_enemy = True
                if not hit_enemy:
                    self.energy += self.upgrade_manager.upgrades["Click Power"]["value"]
                    self.energy = min(self.energy, self.max_energy)
                    # self.score += 1
            self.ui_manager.update_upgrade_buttons(
                self.upgrade_manager.upgrades, self.energy)

        for enemy in self.enemy_manager.enemies[:]:
            if not enemy.active:
                self.enemy_manager.enemies.remove(enemy)
                self.energy -= enemy.damage
                if enemy.type == 3:
                    self.energy -= 20

    def handle_auto_clicker(self):
        if self.upgrade_manager.upgrades["Auto-Clicker"]["level"] > 0 and pyxel.frame_count % 30 == 0:
            self.energy += self.upgrade_manager.upgrades["Auto-Clicker"]["level"]
            self.energy = min(self.energy, self.max_energy)

    def handle_energy_drain(self):
        self.energy -= self.upgrade_manager.upgrades["Efficiency"]["value"]

    def check_game_over(self):
        if self.energy <= 0:
            self.game_over = True

    def reset_game(self):
        self.energy = 50
        self.max_energy = 150
        self.score = 0
        self.level = 1
        self.level_up_requirement = 30
        self.game_over = False
        self.show_upgrades = False
        self.enemy_manager.clear()
        self.upgrade_manager.reset()
        self.ui_manager.update_upgrade_buttons(
            self.upgrade_manager.upgrades, self.energy)

    def draw(self):
        pyxel.cls(0)
        self.draw_top_ui()
        self.ui_manager.upgrade_button.draw(pyxel.mouse_x, pyxel.mouse_y)
        if self.show_upgrades:
            self.draw_upgrade_panel()
        for enemy in self.enemy_manager.enemies:
            enemy.draw()
        if self.game_over:
            self.draw_game_over()

    def draw_top_ui(self):
        pyxel.text(5, 5, f"ENERGY: {int(self.energy)}/{self.max_energy}", 7)
        pyxel.text(5, 15, f"SCORE: {self.score}", 7)
        pyxel.text(5, 25, f"LEVEL: {self.level}", 7)
        progress = min(1.0, self.score / self.level_up_requirement)
        pyxel.rect(5, 35, int(190 * progress), 5, 9)
        pyxel.rectb(5, 35, 190, 5, 13)
        pyxel.text(80, 35, f"NEXT LEVEL: {self.level_up_requirement}", 7)
        energy_ratio = self.energy / self.max_energy
        pyxel.rect(5, 45, int(190 * energy_ratio), 5, 11)
        pyxel.rectb(5, 45, 190, 5, 13)

    def draw_upgrade_panel(self):
        pyxel.rect(5, 55, 190, 120, 1)
        pyxel.rectb(5, 55, 190, 120, 3)
        pyxel.text(75, 60, "UPGRADE SHOP", 7)
        self.ui_manager.close_button.draw(pyxel.mouse_x, pyxel.mouse_y)
        for button in self.ui_manager.upgrade_buttons:
            button.draw(pyxel.mouse_x, pyxel.mouse_y)

    def draw_game_over(self):
        pyxel.rect(50, 80, 100, 60, 1)
        pyxel.rectb(50, 80, 100, 60, 3)
        pyxel.text(65, 90, "GAME OVER", pyxel.frame_count % 16)
        pyxel.text(60, 100, f"Level: {self.level}", 7)
        pyxel.text(60, 110, f"Score: {self.score}", 7)
        restart_color = 11 if (70 <= pyxel.mouse_x <=
                               130 and 110 <= pyxel.mouse_y <= 130) else 8
        pyxel.rect(70, 120, 60, 15, restart_color)
        pyxel.text(85, 123, "RESTART", 0)


IdleClicker()

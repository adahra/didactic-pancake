# title: Pyxel Jump
# author: Takashi Kitao
# desc: A Pyxel simple game example
# site: https://github.com/kitao/pyxel
# license: MIT
# version: 1.0

import pyxel


class App:
    def __init__(self):
        pyxel.init(160, 120, title="Pyxel Jump")
        pyxel.load("assets/jump_game.pyxres")

        self.score = 0
        self.player_x = 72
        self.player_y = -16
        self.player_dy = 0
        self.is_alive = True

        self.far_cloud = [(-10, 75), (40, 65), (90, 60)]
        self.near_cloud = [(10, 25), (70, 35), (120, 15)]

        self.floor = [(i * 60, pyxel.rndi(8, 104), True) for i in range(4)]
        self.fruit = [
            (i * 60, pyxel.rndi(0, 104), pyxel.rndi(0, 2), True) for i in range(4)
        ]

        pyxel.playm(0, loop=True)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.update_player()

        for i, v in enumerate(self.floor):
            self.floor[i] = self.update_floor(*v)

        for i, v in enumerate(self.fruit):
            self.fruit[i] = self.update_fruit(*v)

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            self.player_x = max(self.player_x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)

        self.player_y += self.player_dy
        self.player_dy = min(self.player_dy + 1, 8)

        if self.player_y > pyxel.height:
            if self.is_alive:
                self.is_alive = False
                pyxel.play(3, 5)

            if self.player_y > 600:
                self.score = 0
                self.player_x = 72
                self.player_y = -16
                self.player_dy = 0
                self.is_alive = True

    def update_floor(self, x, y, is_alive):
        if is_alive:
            if (
                self.player_x + 16 >= x
                and self.player_x <= x + 40
                and self.player_y + 16 >= y
                and self.player_y <= y + 8
                and self.player_dy > 0
            ):
                is_alive = False
                self.score += 10
                self.player_dy = -12
                pyxel.play(3, 3)
        else:
            y += 6

        x -= 4

        if x < -40:
            x += 240
            y = pyxel.rndi(8, 104)
            is_alive = True

        return x, y, is_alive

    def update_fruit(self, x, y, kind, is_alive):
        if is_alive and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:
            is_alive = False
            self.score += (kind + 1) * 100
            self.player_dy = min(self.player_dy, -8)
            pyxel.play(3, 4)

        x -= 2

        if x < -40:
            x += 240
            y = pyxel.rndi(0, 104)
            kind = pyxel.rndi(0, 2)
            is_alive = True

        return (x, y, kind, is_alive)

    def draw(self):
        pyxel.cls(12)

        # Draw sky
        pyxel.blt(0, 88, 0, 0, 88, 160, 32)

        # Draw mountain
        pyxel.blt(0, 88, 0, 0, 64, 160, 24, 12)

        # Draw trees
        offset = pyxel.frame_count % 160
        for i in range(2):
            pyxel.blt(i * 160 - offset, 104, 0, 0, 48, 160, 16, 12)

        # Draw clouds
        offset = (pyxel.frame_count // 16) % 160
        for i in range(2):
            for x, y in self.far_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 64, 32, 32, 8, 12)

        offset = (pyxel.frame_count // 8) % 160
        for i in range(2):
            for x, y in self.near_cloud:
                pyxel.blt(x + i * 160 - offset, y, 0, 0, 32, 56, 8, 12)

        # Draw floors
        for x, y, is_alive in self.floor:
            pyxel.blt(x, y, 0, 0, 16, 40, 8, 12)

        # Draw fruits
        for x, y, kind, is_alive in self.fruit:
            if is_alive:
                pyxel.blt(x, y, 0, 32 + kind * 16, 0, 16, 16, 12)

        # Draw player
        pyxel.blt(
            self.player_x,
            self.player_y,
            0,
            16 if self.player_dy > 0 else 0,
            0,
            16,
            16,
            12,
        )

        # Draw score
        s = f"SCORE {self.score:>4}"
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)


App()
# This code creates a simple jump game using the Pyxel library.
# The player controls a character that jumps on platforms and collects fruits.
# The game features a score system, where the player earns points for collecting fruits and jumping on platforms.
# The game also includes a respawn mechanic when the player falls off the screen.
# The game is designed to be simple and easy to understand, making it suitable for beginners.
# The game includes a basic UI displaying the current score.
# The game runs at a fixed frame rate, updating the player's position and drawing the game elements at regular intervals.
# The game features a simple graphics style, with a pixel art aesthetic.
# The game includes sound effects for jumping and collecting items, enhancing the overall experience.
# The game is designed to be fun and engaging, with a focus on simple mechanics and easy controls.
# The game is suitable for all ages and can be played with a keyboard or gamepad.
# The game is a great example of how to create a simple game using the Pyxel library.
# The game can be easily modified and expanded upon, allowing for further development and customization.
# The game is a great starting point for anyone interested in game development or programming.
# The game can be used as a learning tool for beginners, providing a hands-on experience with game development concepts.
# The game can be easily adapted for different platforms and devices, making it versatile and accessible.
# The game can be shared with others, allowing for collaboration and feedback.
# The game can be used as a foundation for more complex projects, providing a solid base for further development.
# The game can be a fun and engaging way to learn programming and game development skills.
# The game can be a great way to practice coding and problem-solving skills.
# The game can be a fun and rewarding experience, providing a sense of accomplishment and satisfaction.

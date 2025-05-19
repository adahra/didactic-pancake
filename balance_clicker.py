import pyxel

class BalanceClicker:
    def __init__(self):
        pyxel.init(160, 120, title="Balance Clicker")
        self.balance = 0
        self.click_value = 1
        self.auto_clicker_cost = 10
        self.auto_clickers = 0
        self.auto_clicker_rate = 1
        self.running = True

        pyxel.run(self.update, self.draw)


    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_SPACE):
            self.balance += self.click_value

        if pyxel.btnp(pyxel.KEY_A) and self.balance >= self.auto_clicker_cost:
            self.balance -= self.auto_clicker_cost
            self.auto_clickers += 1
            self.auto_clicker_cost *= 2

        if pyxel.frame_count % 30 == 0:  # Auto click every second
            self.balance += self.auto_clickers * self.auto_clicker_rate

    def draw(self):
        pyxel.cls(0)
        pyxel.text(10, 10, f"Balance: {self.balance}", 7)
        pyxel.text(10, 20, f"Click Value: {self.click_value}", 7)
        pyxel.text(10, 30, f"Auto Clickers: {self.auto_clickers}", 7)
        pyxel.text(10, 40, f"Auto Clicker Cost: {self.auto_clicker_cost}", 7)
        pyxel.text(10, 50, "Press SPACE to click", 7)
        pyxel.text(10, 60, "Press A to buy auto clicker", 7)
        pyxel.text(10, 70, "Press Q to quit", 7)
        pyxel.flip()


BalanceClicker()
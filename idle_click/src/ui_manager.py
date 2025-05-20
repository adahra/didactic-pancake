from button import Button

class UIManager:
    def __init__(self, upgrade_manager):
        self.upgrade_button = Button(10, 180, 180, 15, "UPGRADES", 5)
        self.close_button = Button(160, 60, 30, 15, "X", 8)
        self.upgrade_buttons = []
        self.update_upgrade_buttons(upgrade_manager.upgrades, 0)

    def update_upgrade_buttons(self, upgrades, energy):
        self.upgrade_buttons = [
            Button(10, 60 + i*25, 180, 20,
                   f"{name} (Lv:{data['level']}) - {data['cost']}pts",
                   9 if energy >= data["cost"] else 8)
            for i, (name, data) in enumerate(upgrades.items())
        ]
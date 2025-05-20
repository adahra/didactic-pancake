class UpgradeManager:
    def __init__(self):
        self.upgrades = {
            "Auto-Clicker": {"level": 0, "cost": 10, "value": 1, "original_cost": 10},
            "Efficiency": {"level": 0, "cost": 15, "value": 0.2, "original_cost": 15},
            "Click Power": {"level": 0, "cost": 20, "value": 5, "original_cost": 20},
            "Slow Shot": {"level": 0, "cost": 25, "value": 3, "original_cost": 25}
        }

    def can_buy(self, name, energy):
        return energy >= self.upgrades[name]["cost"]

    def buy(self, name):
        upgrade = self.upgrades[name]
        upgrade["level"] += 1
        upgrade["cost"] += int(upgrade["cost"] * 0.5)
        if name == "Efficiency":
            upgrade["value"] *= 0.9

    def reset(self):
        for name, upgrade in self.upgrades.items():
            upgrade["level"] = 0
            upgrade["cost"] = upgrade["original_cost"]
            if name == "Efficiency":
                upgrade["value"] = 0.2
            elif name == "Auto-Clicker":
                upgrade["value"] = 1
            elif name == "Click Power":
                upgrade["value"] = 5
            elif name == "Slow Shot":
                upgrade["value"] = 3
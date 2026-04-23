class Effect:
    def execute(self, source, target):
        pass


class DamageEffect(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, source, target):
        target.receive_damage(self.amount)
        print(f"🔥 Hace {self.amount} daño")


class HealEffect(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, source, target):
        source.hp += self.amount
        print(f"💚 Cura {self.amount}")
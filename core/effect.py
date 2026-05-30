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
        # 🔥 FIX: respetar max_hp al curar — antes podía subir HP infinitamente
        source.hp = min(source.hp + self.amount, source.max_hp)
        print(f"💚 Cura {self.amount} (HP: {source.hp}/{source.max_hp})")

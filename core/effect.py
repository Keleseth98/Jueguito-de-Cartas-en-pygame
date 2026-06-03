class Effect:
    def execute(self, source, target):
        pass


class DamageEffect(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, source, target, context=None):
        target.receive_damage(self.amount)
        print(f"🔥 Hace {self.amount} daño")


class CreatureDamageEffect(Effect):
    """Daño a una única criatura (no puede apuntar al héroe)."""
    def __init__(self, amount):
        self.amount = amount

    def apply(self, source, target, context=None):
        target.receive_damage(self.amount)
        print(f"⚡ {self.amount} daño a {target.name}")


class AoeDamageEffect(Effect):
    """Daño a TODAS las criaturas enemigas en el campo."""
    def __init__(self, amount):
        self.amount = amount

    def apply(self, source, target, context=None):
        if context and "battlefield" in context:
            bf = context["battlefield"]
            enemy_creatures = bf.get_enemy_creatures(source)
            if enemy_creatures:
                print(f"💥 AoE — golpea {len(enemy_creatures)} criatura(s)")
                for creature in list(enemy_creatures):
                    creature.receive_damage(self.amount)
                return
        # fallback: si no hay contexto, daño al target normal
        target.receive_damage(self.amount)
        print(f"🔥 AoE (fallback) — {self.amount} daño")


class HealEffect(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, source, target, context=None):
        source.hp = min(source.hp + self.amount, source.max_hp)
        print(f"💚 Cura {self.amount} (HP: {source.hp}/{source.max_hp})")

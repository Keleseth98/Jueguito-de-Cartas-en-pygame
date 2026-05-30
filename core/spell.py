from core.card import Card

class SpellCard(Card):
    def __init__(self, name, mana_cost, effect, image_path):
        # 🔥 FIX: Card.__init__ ya carga la imagen — SpellCard no debe cargarla de nuevo
        # La versión original hacía pygame.image.load() dos veces para el mismo archivo
        super().__init__(name, image_path)

        self.mana_cost = mana_cost
        self.effect = effect

    def play(self, caster, target, context):
        mana = context["mana"]

        if mana < self.mana_cost:
            print("❌ No tienes suficiente mana")
            return False

        context["mana"] -= self.mana_cost

        print(f"✨ {caster.name} usa {self.name}")
        self.effect.apply(caster, target)

        return True

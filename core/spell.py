from core.card import Card
import pygame

class SpellCard(Card):
    def __init__(self, name, mana_cost, effect, image_path):
        super().__init__(name, image_path)

        self.mana_cost = mana_cost
        self.effect = effect

        img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(img, (150, 210))

    def play(self, caster, target, context):
        mana = context["mana"]

        # 🔥 1. validar
        if mana < self.mana_cost:
            print("❌ No tienes suficiente mana")
            return False

        # 🔥 2. pagar costo
        context["mana"] -= self.mana_cost

        # 🔥 3. ejecutar efecto
        print(f"✨ {caster.name} usa {self.name}")
        self.effect.apply(caster, target)

        return True
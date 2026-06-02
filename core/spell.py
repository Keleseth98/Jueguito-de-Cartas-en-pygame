from core.card import Card

class SpellCard(Card):
    def __init__(self, name, mana_cost, effect, image_path, target_type="any"):
        super().__init__(name, image_path)
        self.mana_cost   = mana_cost
        self.effect      = effect
        self.target_type = target_type  # "any" | "creature"

    def play(self, caster, target, context):
        mana = context["mana"]

        if mana < self.mana_cost:
            print("❌ No tienes suficiente mana")
            return False

        # Validar que el target sea criatura si el hechizo lo requiere
        if self.target_type == "creature" and hasattr(target, "is_player"):
            print("❌ Este hechizo requiere una criatura como objetivo")
            return False

        context["mana"] -= self.mana_cost

        game = context.get("game")
        if game:
            from ui.animations.spell_animation import SpellAnimation
            game.animation_queue.append(SpellAnimation(self))

        print(f"✨ {caster.name} usa {self.name} → {target.name}")
        self.effect.apply(caster, target, context)

        return True

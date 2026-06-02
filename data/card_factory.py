from core.creature_card import CreatureCard
from core.spell import SpellCard
from core.effect import DamageEffect, HealEffect, AoeDamageEffect, CreatureDamageEffect

class CardFactory:
    def __init__(self, database):
        self.db = database

    def create(self, card_id):
        data = self.db.get(card_id)

        if data["type"] == "creature":
            return CreatureCard(
                data["name"],
                data["attack"],
                data["health"],
                data["hp_cost"],
                data["image"]
            )

        elif data["type"] == "spell":
            effect_type = data["effect"]

            if effect_type == "damage":
                effect      = DamageEffect(data["value"])
                target_type = "any"
            elif effect_type == "aoe_damage":
                effect      = AoeDamageEffect(data["value"])
                target_type = "any"
            elif effect_type == "creature_damage":
                effect      = CreatureDamageEffect(data["value"])
                target_type = "creature"
            else:
                effect      = HealEffect(data["value"])
                target_type = "any"

            return SpellCard(
                data["name"],
                data["mana_cost"],
                effect,
                data["image"],
                target_type=target_type
            )
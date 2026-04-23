from core.creature_card import CreatureCard
from core.spell import SpellCard
from core.effect import DamageEffect, HealEffect

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
            if data["effect"] == "damage":
                effect = DamageEffect(data["value"])
            else:
                effect = HealEffect(data["value"])

            return SpellCard(
                data["name"],
                data["mana_cost"],
                effect,
                data["image"]
            )
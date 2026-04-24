from core.card import Card
from core.creature import Creature

class CreatureCard(Card):
    def __init__(self, name, attack, health, hp_cost, image_path):
        super().__init__(name, image_path)

        self.attack = attack
        self.health = health
        self.hp_cost = hp_cost

    def play(self, source,target, context):

        if source.hp <= self.hp_cost:
            print("❌ No tienes suficiente HP para invocar")
            return False

        source.hp -= self.hp_cost

        creature = Creature(self, source)

        creature.can_attack = False

        battlefield = context["battlefield"]
        success = battlefield.add_creature(creature, source)

        if not success:
            print("❌ No hay espacio en el campo")
            return False

        print(f"🐲 {source.name} invoca {self.name} ({self.attack}/{self.health})")

        return True
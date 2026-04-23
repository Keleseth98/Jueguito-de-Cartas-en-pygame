from core.card import Card
from core.creature import Creature
import pygame

class CreatureCard:
    def __init__(self, name, attack, health, hp_cost, image_path):
        self.name = name
        self.attack = attack
        self.health = health
        self.hp_cost = hp_cost
        self.image_path = image_path

        img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(img, (150, 210))

    def play(self, source, target, context):
        """
        source: jugador que juega la carta
        target: no se usa por ahora
        context: dict con battlefield, mana, etc.
        """

        # --- validar costo ---
        if source.hp <= self.hp_cost:
            print("❌ No tienes suficiente HP para invocar")
            return False

        # --- pagar costo ---
        source.hp -= self.hp_cost

        # --- crear criatura ---
        creature = Creature(
        name=self.name,
        attack=self.attack,
        health=self.health,
        owner=source,
        image_path=self.image_path   # 🔥 AQUÍ ESTÁ LA CLAVE
        )

        # no puede atacar el turno que entra
        creature.can_attack = False

        # --- agregar al campo ---
        battlefield = context["battlefield"]
        success = battlefield.add_creature(creature, source)

        if not success:
            print("❌ No hay espacio en el campo")
            return False

        print(f"🐲 {source.name} invoca {self.name} ({self.attack}/{self.health})")

        return True
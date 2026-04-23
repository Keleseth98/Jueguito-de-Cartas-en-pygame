import pygame

class Creature:
    def __init__(self, name, attack, health, owner,image_path):
        self.name = name
        self.attack = attack
        self.max_health = health
        self.health = health
        self.image_path = image_path

        self.owner = owner  # referencia al jugador

        img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(img, (150, 210))

        self.can_attack = False
        self.alive = True

    def receive_damage(self, amount):
        self.health = max(0, self.health - amount)
        print(f"💥 {self.name} recibe {amount} daño (HP: {self.health})")

        if self.health <= 0:
            self.alive = False
            print(f"☠️ {self.name} ha muerto")

    def heal(self, amount):
        self.health = min(self.health + amount, self.max_health)
        print(f"💚 {self.name} se cura (HP: {self.health})")

    def enable_attack(self):
        self.can_attack = True

    def disable_attack(self):
        self.can_attack = False

    def attack_target(self, target):
        if not self.can_attack:
            print(f"❌ {self.name} no puede atacar este turno")
            return

        print(f"⚔️ {self.name} ataca a {target.name}")

        # daño al objetivo
        target.receive_damage(self.attack)

        # contraataque si el target también es criatura
        if hasattr(target, "attack"):
            self.receive_damage(target.attack)

        self.can_attack = False

    def is_alive(self):
        return self.alive

    
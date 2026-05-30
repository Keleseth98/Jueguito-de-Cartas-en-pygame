from core.deck import Deck
import pygame

class Character:
    def __init__(self, name, deck, is_player=True, image_path=None):
        self.name = name
        # HP empieza en 5 y crece cada turno hasta el límite de veces configurado
        self.hp = 5
        self.max_hp = 5

        self.is_player = is_player

        self.deck = Deck(deck)
        self.hand = []
        self.discard = []

        self.total_mana_used = 0
        self.creatures = []

        # Prioridad: usar imagen externa si existe
        if image_path:
            path = image_path
        else:
            if is_player:
                path = "assets/heroes/player.png"
            else:
                path = "assets/heroes/enemy.png"

        self.original_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.smoothscale(self.original_image, (150, 210))

    def gain_hp(self, amount):
        # El máximo crece junto con el HP — no es un techo fijo
        self.max_hp += amount
        self.hp += amount

    def is_alive(self):
        return self.hp > 0

    def draw_card(self):
        if len(self.hand) >= 5:
            print("⚠️ Mano llena")
            return None

        card = self.deck.draw()

        if card is None:
            self.reshuffle()
            card = self.deck.draw()

        if card:
            self.hand.append(card)
            return card

        return None

    def receive_damage(self, amount):
        self.hp = max(0, self.hp - amount)
        print(f"💥 {self.name} recibe {amount} de daño (HP: {self.hp})")

        if self.hp == 0:
            self.die()

    def die(self):
        print(f"☠️ {self.name} ha sido derrotado")

    def reshuffle(self):
        print("🔄 Barajando discard...")
        self.deck = Deck(self.discard)
        self.discard = []

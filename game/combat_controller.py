from ui.animations.damage_text import DamageText

class CombatController:
    def __init__(self, battlefield):
        self.battlefield = battlefield

    def select_attacker(self, player):
        print("\n🗡️ Tus criaturas:")

        valid = []

        for i, c in enumerate(self.battlefield.get_player_creatures(player)):
            if c.is_alive() and c.can_attack:
                print(f"{i}: {c.name} ({c.attack}/{c.health})")
                valid.append(i)

        if not valid:
            print("❌ No hay criaturas disponibles")
            return None

        idx = int(input("Elige atacante: "))

        if idx not in valid:
            return None

        return self.battlefield.get_player_creatures(player)[idx]
    
    def select_target(self, player, enemy):
        print("\n🎯 Selecciona objetivo:")

        enemy_creatures = self.battlefield.get_enemy_creatures(player)

        print("0: Héroe enemigo")

        for i, c in enumerate(enemy_creatures, start=1):
            print(f"{i}: {c.name} ({c.attack}/{c.health})")

        choice = int(input("> "))

        if choice == 0:
            return enemy

        idx = choice - 1

        if idx < 0 or idx >= len(enemy_creatures):
            return None

        return enemy_creatures[idx]
    
    def attack(self, player, enemy):
        attacker = self.select_attacker(player)

        if not attacker:
            return

        target = self.select_target(player, enemy)

        if not target:
            return

        attacker.attack_target(target)

        # posición izquierda (atacante)
        self.damage_texts.append(
            DamageText(self.attacker.attack, 250, 450)
        )

        # posición derecha (defensor)
        self.damage_texts.append(
            DamageText(self.defender.attack, 1200, 450)
        )

        self.cleanup()

    def cleanup(self):
        self.battlefield.player_side = [
            c for c in self.battlefield.player_side if c.is_alive()
        ]

        self.battlefield.enemy_side = [
            c for c in self.battlefield.enemy_side if c.is_alive()
        ]
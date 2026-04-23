# game/ai_controller.py

class AIController:
    def __init__(self, battlefield):
        self.battlefield = battlefield

    # -------------------------
    # TURNO COMPLETO IA
    # -------------------------
    def play_turn(self, ai_player, enemy_player, context):
        print("\n🤖 Turno del enemigo")

        # 1. Jugar cartas
        self.play_cards(ai_player, enemy_player, context)

        # 2. Atacar
        self.attack(ai_player, enemy_player)

    # -------------------------
    # JUGAR CARTAS
    # -------------------------
    def play_cards(self, ai, enemy, context):
        """
        IA simple:
        - Intenta jugar todas las cartas posibles
        - Respeta HP (criaturas) y mana (hechizos)
        """

        i = 0

        while i < len(ai.hand):
            card = ai.hand[i]

            if hasattr(card, "mana_cost"):
                if context["mana"] < card.mana_cost:
                    i += 1
                    continue

            # Evitar suicidio con criaturas
            if hasattr(card, "hp_cost"):
                if ai.hp <= card.hp_cost:
                    i += 1
                    continue

            # Intentar jugar carta
            played = card.play(ai, enemy, context)

            if played:
                print(f"🤖 IA juega {card.name}")

                ai.discard.append(card)
                ai.hand.pop(i)

            else:
                i += 1

    # -------------------------
    # ATAQUE
    # -------------------------
    def attack(self, ai, enemy):
        creatures = self.battlefield.get_player_creatures(ai)
        enemy_creatures = self.battlefield.get_enemy_creatures(ai)

        print("\n⚔️ IA ataca")

        for creature in creatures:
            if not creature.is_alive() or not creature.can_attack:
                continue

            target = self.choose_target(creature, enemy, enemy_creatures)

            print(f"🤖 {creature.name} ataca a {target.name}")
            creature.attack_target(target)

        self.cleanup()

    # -------------------------
    # SELECCIÓN DE OBJETIVO
    # -------------------------
    def choose_target(self, creature, enemy, enemy_creatures):
        """
        Prioridad:
        1. Trade favorable (yo sobrevivo, él muere)
        2. Trade neutro (ambos mueren)
        3. Daño eficiente
        4. Héroe si no hay buenas opciones
        """

        best_target = None
        best_score = -999

        for target in enemy_creatures:
            if not target.is_alive():
                continue

            # daño recibido por mi criatura
            damage_taken = target.attack
            survives = creature.health > damage_taken

            # daño que hago
            kills = creature.attack >= target.health

            score = 0

            # 🔥 1. trade perfecto (yo sobrevivo y mato)
            if kills and survives:
                score += 100

            # 🔥 2. trade neutro (ambos mueren)
            elif kills:
                score += 50

            # 🔥 3. daño sin morir
            elif survives:
                score += 20

            # 🔥 penalizar suicidio
            else:
                score -= 20

            # 🔥 pequeño factor aleatorio (para que no sea perfecta)
            import random
            score += random.randint(-5, 5)

            if score > best_score:
                best_score = score
                best_target = target

        # 🔥 decidir si atacar héroe
        if best_target is None:
            return enemy

        # si el trade es muy malo → atacar héroe
        if best_score < 10:
            return enemy

        return best_target

    # -------------------------
    # LIMPIEZA
    # -------------------------
    def cleanup(self):
        self.battlefield.player_side = [
            c for c in self.battlefield.player_side if c.is_alive()
        ]

        self.battlefield.enemy_side = [
            c for c in self.battlefield.enemy_side if c.is_alive()
        ]
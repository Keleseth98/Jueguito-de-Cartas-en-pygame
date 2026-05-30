
class AIController:
    def __init__(self, game, battlefield):
        self.game = game
        self.battlefield = battlefield

        # ESTADO DE ATAQUE
        self.attacking = False
        self.attack_index = 0
        # 🔥 FIX: snapshot de criaturas al inicio del turno para que el índice
        # no se desincronice si alguna criatura muere durante la fase de ataque
        self._attack_creatures_snapshot = []

    # -------------------------
    # TURNO COMPLETO IA
    # -------------------------
    def play_turn(self, ai_player, enemy_player, context):
        print("\n🤖 Turno del enemigo")

        self.play_cards(ai_player, enemy_player, context)

        # 🔥 FIX: activar fase de ataque (antes estaba en False — la IA nunca atacaba)
        self.attacking = True
        self.attack_index = 0
        self._attack_creatures_snapshot = list(
            self.battlefield.get_player_creatures(ai_player)
        )
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
        # Solo procesar si la fase de ataque está activa
        if not self.attacking:
            return

        # 🔥 FIX: esperar que termine la animación actual antes del siguiente ataque
        # Antes se comprobaba current_animation pero también hay que esperar animation_queue
        if self.game.current_animation or self.game.animation_queue:
            return

        enemy_creatures = self.battlefield.get_enemy_creatures(ai)
        # 🔥 FIX: usar snapshot fijo — si se recalcula creatures cada frame
        # y una criatura muere, el índice apunta a la criatura equivocada
        creatures = self._attack_creatures_snapshot

        # recorrer criaturas una por una
        while self.attack_index < len(creatures):
            creature = creatures[self.attack_index]
            self.attack_index += 1

            if not creature.is_alive() or not creature.can_attack:
                continue

            target = self.choose_target(creature, enemy, enemy_creatures)

            print(f"🤖 {creature.name} ataca a {target.name}")

            self.game.resolve_attack(creature, target)
            return  # solo un ataque por frame, esperar animación

        # Todos los ataques terminaron
        print("✅ IA terminó de atacar")
        self.attacking = False
        self._attack_creatures_snapshot = []
        self.cleanup()
        # 🔥 FIX: cerrar el ciclo de turno AQUÍ, no en end_turn()
        # Garantiza que finish_turn_cycle ocurre DESPUÉS de todas las animaciones
        self.game.finish_turn_cycle()

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

            # 1. trade perfecto (yo sobrevivo y mato)
            if kills and survives:
                score += 100

            # 2. trade neutro (ambos mueren)
            elif kills:
                score += 50

            # 3. daño sin morir
            elif survives:
                score += 20

            #  penalizar suicidio
            else:
                score -= 20

            #  pequeño factor aleatorio (para que no sea perfecta)
            import random
            score += random.randint(-5, 5)

            if score > best_score:
                best_score = score
                best_target = target

        # decidir si atacar héroe
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
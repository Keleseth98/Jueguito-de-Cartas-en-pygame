
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
        i = 0
        while i < len(ai.hand):
            card = ai.hand[i]

            if hasattr(card, "mana_cost"):
                if context["mana"] < card.mana_cost:
                    i += 1
                    continue

            if hasattr(card, "hp_cost"):
                if ai.hp <= card.hp_cost:
                    i += 1
                    continue

            # Determinar target según tipo de hechizo
            target = enemy  # default: héroe enemigo

            if getattr(card, "target_type", "any") == "creature":
                best = self._choose_spell_target(card, context)
                if best is None:
                    # No hay criaturas válidas, no jugar esta carta
                    i += 1
                    continue
                target = best

            played = card.play(ai, target, context)

            if played:
                print(f"🤖 IA juega {card.name} → {target.name}")
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

    def _choose_spell_target(self, card, context):
        """
        Elige la mejor criatura enemiga para un hechizo dirigido.
        Prioridad:
          1. Criatura que muere exactamente con el daño (valor máximo)
          2. Criatura con más ataque (amenaza mayor)
          3. Cualquier criatura viva
        Devuelve None si no hay criaturas enemigas.
        """
        # Las criaturas enemigas de la IA son las del lado del jugador
        targets = self.battlefield.player_side
        alive   = [c for c in targets if c.is_alive()]

        if not alive:
            return None

        damage = getattr(card.effect, "amount", 0)

        best       = None
        best_score = -999

        for c in alive:
            score = 0
            if c.health <= damage:          # hechizo la mata
                score += 100
            score += c.attack * 5           # priorizar amenazas altas
            score -= c.health               # preferir las más débiles

            if score > best_score:
                best_score = score
                best       = c

        return best

    # -------------------------
    # SELECCIÓN DE OBJETIVO (ataque de criatura)
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
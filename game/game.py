from ui.animations.combat_animation import CombatAnimation

class Game:
    def __init__(self, player, enemy, battlefield):
        self.player = player
        self.enemy = enemy
        self.battlefield = battlefield

        # HP por turnos — contadores separados por personaje
        # El jugador sube HP 4 veces, el enemigo usa hp_growth_turns del JSON (se sobreescribe en main.py)
        self.player_hp_turns = 0
        self.player_max_hp_turns = 4  # el jugador escala 4 veces

        self.enemy_hp_turns = 0
        self.enemy_max_hp_turns = 2   # se sobreescribe desde enemy_data["hp_growth_turns"]

        #  Mana por turnos 
        self.mana_turns = 0
        self.max_mana_turns = 5
        self.max_mana = 20

        # Turnos
        self.turn = 1
        self.is_player_turn = True

        # Mana actual
        self.player_mana = 1
        self.enemy_mana = 1

        #Tiempos de animacion de mano inicial
        self.initial_draw_queue = []
        self.draw_timer = 0
        self.draw_interval = 0.3  # segundos entre cartas

        self.animation_queue = []
        self.current_animation = None

        self.game_over = False

    # -------------------------
    # FIN DE TURNO
    # -------------------------
    def end_turn(self):
        if self.game_over:
            return

        if self.is_player_turn:
            print("🔁 Fin de turno (jugador)")

            self.is_player_turn = False

            # turno IA: juega cartas y activa self.ai.attacking = True
            self.run_enemy_turn()

            if self.check_game_over():
                return

            # 🔥 FIX: finish_turn_cycle ya NO se llama aquí
            # Lo llama ai.attack() cuando termina todos sus ataques

    # -------------------------
    # TURNO IA
    # -------------------------
    def run_enemy_turn(self):
        print("\n🤖 Turno del enemigo")

        context = {
            "mana": self.enemy_mana,
            "battlefield": self.battlefield
        }

        self.ai.play_turn(self.enemy, self.player, context)

        self.enemy_mana = context["mana"]

    def resolve_attack(self, attacker, target):
        if self.game_over:
            return

        from ui.animations.combat_animation import CombatAnimation

        #  crear animación 
        self.animation_queue.append(
            CombatAnimation(attacker, target))

        #  lógica
        attacker.attack_target(target)
        attacker.can_attack = False

        self.combat_controller.cleanup()
        self.check_game_over()

    # -------------------------
    # CIERRE DE CICLO (NUEVO TURNO)
    # -------------------------
    def finish_turn_cycle(self):
        if self.game_over:
            return

        print("🔁 Inicio de turno del jugador")

        self.turn += 1

        # -------- MANA --------
        if self.mana_turns < self.max_mana_turns:
            self.mana_turns += 1
            new_mana = min(self.player_mana + 1, self.max_mana)

            self.player_mana = new_mana
            self.enemy_mana = new_mana

        # -------- VIDA --------
        # Cada personaje tiene su propio contador de veces que puede crecer
        if self.player_hp_turns < self.player_max_hp_turns:
            self.player_hp_turns += 1
            self.player.gain_hp(5)
            print(f"❤️ Jugador: HP {self.player.hp}/{self.player.max_hp}")

        if self.enemy_hp_turns < self.enemy_max_hp_turns:
            self.enemy_hp_turns += 1
            self.enemy.gain_hp(5)
            print(f"❤️ Enemigo: HP {self.enemy.hp}/{self.enemy.max_hp}")

        # activar criaturas
        for c in self.battlefield.player_side:
            c.enable_attack()

        for c in self.battlefield.enemy_side:
            c.enable_attack()

        # robar cartas
        card = self.player.draw_card()
        if card:
            self.renderer.on_card_draw(card, True)

        card = self.enemy.draw_card()
        if card:
            self.renderer.on_card_draw(card, False)

        # turno vuelve al jugador
        self.is_player_turn = True

    def update(self, dt):
        # -------------------------
        # ANIMACIONES DE COMBATE
        # -------------------------
        if not self.current_animation and self.animation_queue:
            self.current_animation = self.animation_queue.pop(0)

        if self.current_animation:
            self.current_animation.update(dt)

            if self.current_animation.finished:
                self.current_animation = None


        # -------------------------
        # ROBO INICIAL 
        # -------------------------
        if self.initial_draw_queue:
            self.draw_timer += dt

            if self.draw_timer >= self.draw_interval:
                self.draw_timer = 0

                who = self.initial_draw_queue.pop(0)

                if who == "player":
                    card = self.player.draw_card()
                    if card:
                        self.renderer.on_card_draw(card, True)
                else:
                    card = self.enemy.draw_card()
                    if card:
                        self.renderer.on_card_draw(card, False)

        # 🔥 FIX: la IA solo ataca si el reparto inicial ya terminó
        if not self.is_player_turn and not self.game_over and not self.initial_draw_queue:
            self.ai.attack(self.enemy, self.player)

    # -------------------------
    # GAME OVER
    # -------------------------
    def check_game_over(self):
        if self.player.hp <= 0:
            print("💀 PERDISTE")
            self.game_over = True
            return True

        if self.enemy.hp <= 0:
            print("🏆 GANASTE")
            self.game_over = True
            return True

        return False
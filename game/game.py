from ui.animations.combat_animation import CombatAnimation

class Game:
    def __init__(self, player, enemy, battlefield):
        self.player = player
        self.enemy = enemy
        self.battlefield = battlefield

        # HP por turnos 
        self.hp_turns = 0
        self.max_hp_turns = 5

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

            # turno IA
            self.run_enemy_turn()

            if self.check_game_over():
                return

            # cerrar turno enemigo
            self.finish_turn_cycle()

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

        # actualizar mana restante
        self.enemy_mana = context["mana"]

    def resolve_attack(self, attacker, target):
        if self.game_over:
            return

        from ui.animations.combat_animation import CombatAnimation

        #  crear animación 
        self.current_animation = CombatAnimation(attacker, target)

        #  lógica
        attacker.attack_target(target)
        attacker.can_attack = False

        self.combat_controller.cleanup()
        self.check_game_over()

    # -------------------------
    # CIERRE DE CICLO (NUEVO TURNO)
    # -------------------------
    def finish_turn_cycle(self):
        print("🔁 Fin de turno (enemigo)")

        self.turn += 1

        # -------- MANA --------
        if self.mana_turns < self.max_mana_turns:
            self.mana_turns += 1
            new_mana = min(self.player_mana + 1, self.max_mana)

            self.player_mana = new_mana
            self.enemy_mana = new_mana

        # -------- VIDA --------
        if self.hp_turns < self.max_hp_turns:
            self.hp_turns += 1
            self.player.gain_hp(5)
            self.enemy.gain_hp(5)

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
        # sistema de robo inicial
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
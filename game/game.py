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
        self.player.draw_card()
        self.enemy.draw_card()

        # turno vuelve al jugador
        self.is_player_turn = True

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
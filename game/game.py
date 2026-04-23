
class Game:
    def __init__(self, player, enemy, battlefield):
        self.player = player
        self.enemy = enemy
        self.battlefield = battlefield
        self.hp_turns = 0  #cuántas veces ya subiste HP
        self.max_hp_turns = 5

        self.turn = 1
        self.is_player_turn = True
        self.player_mana = 1
        self.enemy_mana = 1
        self.game_over = False

    def end_turn(self):
        if self.game_over:
            return

        if self.is_player_turn:
            print("🔁 Fin de turno (jugador)")

            self.is_player_turn = False

            # 🔥 ejecutar IA
            self.run_enemy_turn()

            # 🔥 verificar fin del juego
            if self.check_game_over():
                return

            # 🔥 ahora termina turno enemigo
            self.finish_enemy_turn()

        else:
            self.finish_enemy_turn()
        

    
    def run_enemy_turn(self):
        print("\n🤖 Turno del enemigo")

        # usar mana del turno actual
        context = {
            "mana": self.enemy_mana,
            "battlefield": self.battlefield
        }

        self.ai.play_turn(self.enemy, self.player, context)

        # actualizar mana después de IA
        self.enemy_mana = context["mana"]

    def finish_enemy_turn(self):
        print("🔁 Fin de turno (enemigo)")

        self.turn += 1

        # calcular mana del turno
        new_mana = min(self.turn, 20)

        # asignar mana a ambos jugadores
        self.player_mana = new_mana
        self.enemy_mana = new_mana

        if self.turn <= 6:
            self.player.gain_hp(5)
            self.enemy.gain_hp(5)

        for c in self.battlefield.player_side:
            c.enable_attack()

        for c in self.battlefield.enemy_side:
            c.enable_attack()

        self.player.draw_card()
        self.enemy.draw_card()

        self.is_player_turn = True

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
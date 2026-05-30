class Battlefield:
    def __init__(self):
        self.player_side = []
        self.enemy_side = []
        self.max_slots = 3

    def add_creature(self, creature, owner):
        # 🔥 FIX: usar is_player en vez de comparar nombre hardcodeado "Jugador"
        # Si se cambia el nombre del personaje o se añade un segundo jugador, no rompe
        side = self.player_side if owner.is_player else self.enemy_side

        if len(side) >= self.max_slots:
            print("❌ Campo lleno")
            return False

        side.append(creature)
        return True

    def get_player_creatures(self, player):
        return self.player_side if player.is_player else self.enemy_side

    def get_enemy_creatures(self, player):
        return self.enemy_side if player.is_player else self.player_side

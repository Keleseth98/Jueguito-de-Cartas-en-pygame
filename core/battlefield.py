class Battlefield:
    def __init__(self):
        self.player_side = []
        self.enemy_side = []
        self.max_slots = 3

    def add_creature(self, creature, owner):
        side = self.player_side if owner.name == "Jugador" else self.enemy_side

        if len(side) >= self.max_slots:
            print("❌ Campo lleno")
            return False

        side.append(creature)
        return True
    

    def get_player_creatures(self, player):
        return self.player_side if player.is_player else self.enemy_side

    def get_enemy_creatures(self, player):
        return self.enemy_side if player.is_player else self.player_side
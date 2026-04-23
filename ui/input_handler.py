from utils import constants as cs

class InputHandler:
    def __init__(self, game):
        self.game = game

        self.selected_creature = None
        self.attack_mode = False

    def play_card(self, index):
        context = {
            "mana": self.game.player_mana,
            "battlefield": self.game.battlefield
        }

        player = self.game.player
        enemy = self.game.enemy

        card = player.hand[index]

        success = card.play(player, enemy, context)

        if success:
            player.discard.append(card)
            player.hand.pop(index)

            self.game.player_mana = context["mana"]

    
    def handle_cards_click(self, pos):
        for i, card in enumerate(self.game.player.hand):
            if hasattr(card, "rect") and card.rect.collidepoint(pos):
                self.play_card(i)
                return True

        return False
        
    def select_player_creature(self, pos):
        x, y = pos

        # obtener criaturas
        creatures = self.game.battlefield.get_player_creatures(self.game.player)

        # posiciones del renderer
        start_x, start_y = self.game.renderer.player_start
        spacing = self.game.renderer.spacing

        for i, creature in enumerate(creatures):
            cx = start_x + i * spacing
            cy = start_y

            if cx <= x <= cx + cs.SUMMONED_CARD_WIDTH and cy <= y <= cy + cs.SUMMONED_CARD_HEIGHT:

                # feedback si no puede atacar
                if not creature.can_attack:
                    print(f"❌ {creature.name} aún no puede atacar (summoning sickness)")
                    return True

                # seleccionar criatura
                self.selected_creature = creature
                self.attack_mode = True

                print(f"🟢 Seleccionaste {creature.name}")
                return True

        return False
    
    def select_target(self, pos):
        x, y = pos

        enemy_creatures = self.game.battlefield.get_enemy_creatures(self.game.player)
        start_x, start_y = self.game.renderer.enemy_start
        spacing = self.game.renderer.spacing

        # 🔥 criaturas enemigas
        for i, creature in enumerate(enemy_creatures):
            cx = start_x + i * spacing
            cy = start_y

            if cx <= x <= cx + cs.SUMMONED_CARD_WIDTH and cy <= y <= cy + cs.SUMMONED_CARD_HEIGHT:
                self.attack(creature)
                return True

        # 🔥 héroe enemigo
        if 30 <= x <= 350 and 20 <= y <= 85:
            self.attack(self.game.enemy)
            return True

        return False
    
    def attack(self, target):
        attacker = self.selected_creature

        if not attacker:
            return

        # AQUÍ llama al modelo attack_target
        attacker.attack_target(target)

        # desactivar ataque
        attacker.can_attack = False

        # limpiar muertos
        self.game.combat_controller.cleanup()

        # revisar fin del juego
        if self.game.check_game_over():
            return

        # reset selección
        self.selected_creature = None
        self.attack_mode = False

    def handle_click(self, pos):
        if not self.game.is_player_turn or self.game.game_over:
            return

        x, y = pos

        # botón turno
        if self.game.renderer.end_turn_rect.collidepoint(x, y):
            self.end_turn()
            return

        # 🔥 1. seleccionar criatura
        if self.select_player_creature(pos):
            return

        # 🔥 2. atacar si ya seleccionó
        if self.attack_mode:
            if self.select_target(pos):
                return

        # cartas
        if self.handle_cards_click(pos):
            return
    
    def end_turn(self):
        print("🔁 Fin de turno (jugador)")
        self.game.end_turn()

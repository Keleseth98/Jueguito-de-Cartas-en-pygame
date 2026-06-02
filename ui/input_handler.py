from utils import constants as cs
from ui.animations.combat_animation import CombatAnimation

class InputHandler:
    def __init__(self, game):
        self.game = game

        self.selected_creature  = None
        self.attack_mode        = False

        # Estado para hechizos que requieren objetivo criatura
        self.spell_targeting_mode = False
        self.pending_spell_index  = None   # índice en player.hand

    def play_card(self, index, target=None):
        context = {
            "mana": self.game.player_mana,
            "battlefield": self.game.battlefield,
            "game": self.game
        }

        player = self.game.player
        enemy  = self.game.enemy
        card   = player.hand[index]

        # Hechizo que necesita criatura: si no hay target todavía, entrar en modo selección
        if getattr(card, "target_type", "any") == "creature" and target is None:
            enemy_creatures = self.game.battlefield.get_enemy_creatures(player)
            if not enemy_creatures:
                print("❌ No hay criaturas enemigas para apuntar")
                return False
            self.spell_targeting_mode = True
            self.pending_spell_index  = index
            print(f"🎯 Selecciona una criatura enemiga para {card.name}")
            return False   # no jugar todavía

        # Target resuelto (o hechizo sin objetivo específico)
        resolved_target = target if target is not None else enemy
        success = card.play(player, resolved_target, context)

        if success:
            player.discard.append(card)
            player.hand.pop(index)
            self.game.player_mana = context["mana"]
            self._cancel_spell_targeting()

        return success

    def _cancel_spell_targeting(self):
        self.spell_targeting_mode = False
        self.pending_spell_index  = None

    # --------------------------------------------------
    def handle_cards_click(self, pos):
        for i, card in enumerate(self.game.player.hand):
            if hasattr(card, "rect") and card.rect.collidepoint(pos):
                self.play_card(i)
                return True
        return False

    def select_player_creature(self, pos):
        x, y = pos
        creatures = self.game.battlefield.get_player_creatures(self.game.player)
        start_x, start_y = self.game.renderer.player_start
        spacing = self.game.renderer.spacing

        for i, creature in enumerate(creatures):
            cx = start_x + i * spacing
            cy = start_y
            if cx <= x <= cx + cs.SUMMONED_CARD_WIDTH and cy <= y <= cy + cs.SUMMONED_CARD_HEIGHT:
                if not creature.can_attack:
                    print(f"❌ {creature.name} aún no puede atacar (summoning sickness)")
                    return True
                self.selected_creature = creature
                self.attack_mode = True
                print(f"🟢 Seleccionaste {creature.name}")
                return True
        return False

    def select_target(self, pos):
        """Selección de objetivo para ATAQUE de criatura."""
        x, y = pos
        enemy_creatures = self.game.battlefield.get_enemy_creatures(self.game.player)
        start_x, start_y = self.game.renderer.enemy_start
        spacing = self.game.renderer.spacing

        for i, creature in enumerate(enemy_creatures):
            cx = start_x + i * spacing
            cy = start_y
            if cx <= x <= cx + cs.SUMMONED_CARD_WIDTH and cy <= y <= cy + cs.SUMMONED_CARD_HEIGHT:
                self.attack(creature)
                return True

        # Héroe enemigo
        if 30 <= x <= 350 and 20 <= y <= 85:
            self.attack(self.game.enemy)
            return True

        return False

    def select_spell_target(self, pos):
        """Selección de criatura objetivo para hechizo con target_type='creature'."""
        x, y = pos
        enemy_creatures = self.game.battlefield.get_enemy_creatures(self.game.player)
        start_x, start_y = self.game.renderer.enemy_start
        spacing = self.game.renderer.spacing

        for i, creature in enumerate(enemy_creatures):
            cx = start_x + i * spacing
            cy = start_y
            if cx <= x <= cx + cs.SUMMONED_CARD_WIDTH and cy <= y <= cy + cs.SUMMONED_CARD_HEIGHT:
                self.play_card(self.pending_spell_index, target=creature)
                return True

        # Clic fuera de criatura → cancelar
        print("❌ Objetivo inválido, cancelando hechizo")
        self._cancel_spell_targeting()
        return True

    def attack(self, target):
        attacker = self.selected_creature
        if not attacker:
            return
        self.game.resolve_attack(attacker, target)
        self.selected_creature = None
        self.attack_mode = False

    def handle_click(self, pos):
        if self.game.current_animation or self.game.animation_queue:
            return
        if not self.game.is_player_turn or self.game.game_over:
            return

        x, y = pos

        # Botón fin de turno
        if self.game.renderer.end_turn_rect.collidepoint(x, y):
            self._cancel_spell_targeting()
            self.end_turn()
            return

        # Modo selección de objetivo de hechizo
        if self.spell_targeting_mode:
            self.select_spell_target(pos)
            return

        # Modo ataque de criatura
        if self.attack_mode:
            if self.select_target(pos):
                return

        # Seleccionar criatura propia para atacar
        if self.select_player_creature(pos):
            return

        # Jugar carta de la mano
        if self.handle_cards_click(pos):
            return

    def end_turn(self):
        print("🔁 Fin de turno (jugador)")
        self.game.end_turn()

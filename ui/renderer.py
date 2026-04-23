import pygame
from utils import constants as cs

class Renderer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.card_width = 120
        self.card_height = 210
        self.spacing = 180  # ajusta según tu diseño

        # POSICIONES EXACTAS DE CASILLAS DE INVOCACION DE CARTA
        self.player_start = (342, 438)
        self.enemy_start = (342, 175)

        self.background = pygame.image.load("assets/boards/board1.jpg").convert_alpha()
        self.background = pygame.transform.smoothscale(self.background, (cs.SCREEN_WIDTH, cs.SCREEN_HEIGHT))

    def draw(self):
        self.draw_battlefield()
        self.draw_creatures()
        self.draw_hand()
        self.draw_ui()
        self.end_turn_rect = self.draw_end_turn_button()

    def draw_battlefield(self):
        self.screen.blit(self.background, (0, 0))

    def draw_creatures(self):
        """
        Dibuja todas las criaturas en el campo usando
        posiciones fijas definidas en el renderer.
        """

        # 🔥 Criaturas del jugador
        player_creatures = self.game.battlefield.player_side
        self.draw_row(player_creatures, self.player_start)

        # 🔥 Criaturas del enemigo
        enemy_creatures = self.game.battlefield.enemy_side
        self.draw_row(enemy_creatures, self.enemy_start)

    def draw_row(self, creatures, start_pos):
        start_x, y = start_pos

        for i, creature in enumerate(creatures):
            x = start_x + i * self.spacing
            self.draw_creature(creature, x, y)

    def draw_creature(self, creature, x, y):
        rect = pygame.Rect(x, y, self.card_width, self.card_height)

        # 🔥 color base
        self.screen.blit(creature.image, (x, y))

        # 🔥 HIGHLIGHT (AQUÍ VA)
        selected = self.game.input_handler.selected_creature

        if selected == creature:
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)  # borde amarillo

        # 🔥 texto stats
        font = pygame.font.Font(None, 24)
        text = font.render(f"{creature.attack}/{creature.health}", True, (255, 255, 255))
        self.screen.blit(text, (x + 10, y + 70))

    def draw_hand(self):
        player = self.game.player

        for i, card in enumerate(player.hand):
            x = 500 + i * self.spacing
            y = 800

            # 🔥 crear rect (CLAVE)
            card.rect = pygame.Rect(x, y, self.card_width, self.card_height)

            # 🔥 dibujar carta
            self.screen.blit(card.image, (x, y))

            # 🔥 hover (usando rect)
            mx, my = pygame.mouse.get_pos()
            if card.rect.collidepoint(mx, my):
                pygame.draw.rect(self.screen, (255, 255, 0), card.rect, 3)
        
    def draw_ui(self):
        font = pygame.font.Font(None, 30)

        player = self.game.player
        enemy = self.game.enemy

        # -------------------------
        # HP
        # -------------------------
        hp_text = font.render(f"HP: {player.hp}", True, (255, 255, 255))
        self.screen.blit(hp_text, (50, 835))

        enemyHP_text = font.render(f"Enemy HP: {enemy.hp}", True, (255, 255, 255))
        self.screen.blit(enemyHP_text, (50, 40))

        # -------------------------
        # MANA 
        # -------------------------
        player_text = font.render(f"Mana: {self.game.player_mana}", True, (255, 255, 0))
        self.screen.blit(player_text, (1420, 805))

        enemy_text = font.render(f"Mana: {self.game.enemy_mana}", True, (255, 255, 0))
        self.screen.blit(enemy_text, (1420, 50))


    def draw_end_turn_button(self):
        rect = pygame.Rect((cs.SCREEN_WIDTH - 200 ), (cs.SCREEN_HEIGHT / 2), 120, 50)

        pygame.draw.rect(self.screen, (200, 100, 100), rect)

        font = pygame.font.Font(None, 30)
        text = font.render("End Turn", True, (255, 255, 255))

        self.screen.blit(text, (rect.x + 10, rect.y + 10))

        return rect
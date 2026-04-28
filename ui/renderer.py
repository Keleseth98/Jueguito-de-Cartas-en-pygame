import pygame
from utils import constants as cs

class Renderer:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game

        self.card_width = 120
        self.card_height = 210
        self.spacing = 180  # ajusta según tu diseño

        #POSICIONES DE LOS DECK
        self.deck_pos = (1450, 600)  
        self.enemy_deck_pos = (1400, 100)

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
        self.draw_preview()
        self.draw_animation()
        
        self.end_turn_rect = self.draw_end_turn_button()

    def draw_preview(self):
        for creature in self.game.battlefield.player_side + self.game.battlefield.enemy_side:

            if getattr(creature, "preview_active", False):

                # 🔥 usar imagen ORIGINAL
                big_image = pygame.transform.smoothscale(
                    creature.original_image,
                    (300, 420)   # o el tamaño que quieras
                )

                self.screen.blit(big_image, (50, 200))

    def draw_battlefield(self):
        self.screen.blit(self.background, (0, 0))

    def draw_creatures(self):
        """
        Dibuja todas las criaturas en el campo usando
        posiciones fijas definidas en el renderer.
        """

        #  Criaturas del jugador
        player_creatures = self.game.battlefield.player_side
        self.draw_row(player_creatures, self.player_start)

        #  Criaturas del enemigo
        enemy_creatures = self.game.battlefield.enemy_side
        self.draw_row(enemy_creatures, self.enemy_start)

    def draw_row(self, creatures, start_pos):
        start_x, y = start_pos

        for i, creature in enumerate(creatures):
            x = start_x + i * self.spacing
            self.draw_creature(creature, x, y)

    def draw_animation(self):
        anim = self.game.current_animation

        if not anim:
            return

        dt = getattr(self.game, "delta_time", 0)

        anim.update(dt)
        anim.draw(self.screen)

        if anim.finished:
            self.game.current_animation = None

    def draw_creature(self, creature, x, y):
        

        # rect (hitbox)
        rect = pygame.Rect(x, y, self.card_width, self.card_height)
        creature.rect = rect  # útil para otras partes

        # inicializar variables si no existen
        if not hasattr(creature, "hover_time"):
            creature.hover_time = 0
            creature.preview_active = False

        # mouse + tiempo
        mx, my = pygame.mouse.get_pos()
        dt = getattr(self.game, "delta_time", 0)

        if rect.collidepoint(mx, my):
            creature.hover_time += dt

            # clamp (evita valores absurdos)
            if creature.hover_time > 1:
                creature.hover_time = 1

            creature.preview_active = creature.hover_time >= 1
        else:
            creature.hover_time = 0
            creature.preview_active = False

        # dibujar carta
        self.screen.blit(creature.image, (x, y))

        # HIGHLIGHT (selección para atacar)
        selected = self.game.input_handler.selected_creature
        if selected == creature:
            pygame.draw.rect(self.screen, (255, 255, 0), rect, 3)

        # stats
        font = pygame.font.Font(None, 24)
        text = font.render(f"{creature.attack}/{creature.health}", True, (255, 255, 255))
        self.screen.blit(text, (x + 10, y + 70))

    def on_card_draw(self, card, is_player=True):
        if is_player:
            x, y = self.deck_pos
        else:
            x, y = self.enemy_deck_pos

        card.render_x = x
        card.render_y = y
        card.scale = 1.0

    def draw_hand(self):
        player = self.game.player
        mx, my = pygame.mouse.get_pos()

        for i, card in enumerate(player.hand):
            x = 500 + i * self.spacing
            y = 800

            # inicializar render (solo una vez)
            if not hasattr(card, "render_x"):
                card.render_x = x
                card.render_y = y
                card.scale = 1.0

            # target dinámico
            target_x = x
            is_hover = False

            # rect temporal para hover (usar posición target)
            temp_rect = pygame.Rect(x, y, 150, 210)
            if temp_rect.collidepoint(mx, my):
                is_hover = True

            # targets
            target_y = y - 40 if is_hover else y
            target_scale = 1.1 if is_hover else 1.0

            speed = 0.2

            # interpolación 
            card.render_x += (target_x - card.render_x) * speed
            card.render_y += (target_y - card.render_y) * speed
            card.scale += (target_scale - card.scale) * speed

            # render con escala
            width = int(150 * card.scale)
            height = int(210 * card.scale)

            img = pygame.transform.smoothscale(card.image, (width, height))

            self.screen.blit(img, (card.render_x, card.render_y))

            # actualizar rect FINAL 
            card.rect = pygame.Rect(card.render_x, card.render_y, width, height)


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
        self.screen.blit(enemy_text, (1420, 100))


    def draw_end_turn_button(self):
        rect = pygame.Rect((cs.SCREEN_WIDTH - 200 ), (cs.SCREEN_HEIGHT / 2), 120, 50)

        pygame.draw.rect(self.screen, (200, 100, 100), rect)

        font = pygame.font.Font(None, 30)
        text = font.render("End Turn", True, (255, 255, 255))

        self.screen.blit(text, (rect.x + 10, rect.y + 10))

        return rect
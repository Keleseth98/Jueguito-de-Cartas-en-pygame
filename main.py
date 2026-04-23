import pygame

from ui.renderer import Renderer
from ui.input_handler import InputHandler
from game.game import Game
from core.character import Character
from core.battlefield import Battlefield
from game.ai_controller import AIController
from game.combat_controller import CombatController
from data.card_database import CardDatabase
from data.card_factory import CardFactory

pygame.init()


#inicializar database
db = CardDatabase("data/cards.json")
factory = CardFactory(db)

# -------------------------
# DECK
# -------------------------

def create_deck(factory):
    deck_ids = [
        "lobo", "lobo",
        "guerrero",
        "fireball", "fireball",
        "heal"
    ]

    return [factory.create(card_id) for card_id in deck_ids]
# INIT
# -------------------------
screen = pygame.display.set_mode((1600, 900))
clock = pygame.time.Clock()

battlefield = Battlefield()

player = Character("Jugador", create_deck(factory), is_player=True)
enemy = Character("Enemigo", create_deck(factory), is_player=False)

game = Game(player, enemy, battlefield)

renderer = Renderer(screen, game)
input_handler = InputHandler(game)

game.renderer = renderer
game.input_handler = input_handler

ai = AIController(battlefield)
game.ai = ai

combat_controller = CombatController(battlefield)

game.combat_controller = combat_controller




# mano inicial
for _ in range(3):
    player.draw_card()
    enemy.draw_card()




# -------------------------
# LOOP
# -------------------------
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            input_handler.handle_click(pygame.mouse.get_pos())

        if input_handler.attack_mode:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    renderer.draw()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
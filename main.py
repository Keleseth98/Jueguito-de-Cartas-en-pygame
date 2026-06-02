import pygame

from ui.menu import MainMenu
from ui.reward_screen import RewardScreen
from ui.renderer import Renderer
from ui.input_handler import InputHandler
from game.game import Game
from core.character import Character
from core.deck import Deck
from core.battlefield import Battlefield
from game.ai_controller import AIController
from game.combat_controller import CombatController
from data.card_database import CardDatabase
from data.card_factory import CardFactory
from data.enemy_database import EnemyDatabase
from data.enemy_factory import EnemyFactory

pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("Jueguito de Cartas")
clock = pygame.time.Clock()

# -------------------------
# BASES DE DATOS
# -------------------------
db            = CardDatabase("data/cards.json")
factory       = CardFactory(db)
enemy_db      = EnemyDatabase("data/enemies.json")
enemy_factory = EnemyFactory(factory, enemy_db)

# -------------------------
# SECUENCIA DE ENEMIGOS
# El juego avanza por esta lista en orden.
# Para añadir un nuevo enemigo basta con agregar su id aquí.
# -------------------------
ENEMY_SEQUENCE = [
    "hermitano",
    "bestia",
    "mago",
    "caballero"
]

# -------------------------
# DECK INICIAL DEL JUGADOR
# -------------------------
PLAYER_DECK_IDS = [
    "lobo", "lobo",
    "guerrero",
    "fireball", "fireball",
    "heal"
]

def build_deck(card_ids):
    return [factory.create(cid) for cid in card_ids]

# Estado global de la run
player_deck_ids  = list(PLAYER_DECK_IDS)
current_enemy_idx = 0   # índice en ENEMY_SEQUENCE

# Mapa nombre → id para la pantalla de recompensa
name_to_id = {data["name"]: cid for cid, data in db.cards.items()}

# -------------------------
# INICIAR COMBATE
# -------------------------
def start_game(deck_ids, enemy_id):
    enemy, enemy_data = enemy_factory.create(enemy_id)

    battlefield = Battlefield()
    player      = Character("Jugador", build_deck(deck_ids), is_player=True)

    game = Game(player, enemy, battlefield)
    game.enemy_max_hp_turns = enemy_data["hp_growth_turns"]

    renderer      = Renderer(screen, game)
    input_handler = InputHandler(game)

    game.renderer         = renderer
    game.input_handler    = input_handler
    game.ai               = AIController(game, battlefield)
    game.combat_controller = CombatController(battlefield)

    game.initial_draw_queue = [
        "player", "player", "player",
        "enemy",  "enemy",  "enemy"
    ]

    return game, renderer, input_handler

def reset_run():
    """Reinicia la run completa desde el principio."""
    global player_deck_ids, current_enemy_idx
    player_deck_ids   = list(PLAYER_DECK_IDS)
    current_enemy_idx = 0

# -------------------------
# ESTADOS
# -------------------------
STATE_MENU   = "menu"
STATE_GAME   = "game"
STATE_REWARD = "reward"

state         = STATE_MENU
menu          = MainMenu(screen)
game          = None
renderer      = None
input_handler = None
reward        = None

# -------------------------
# LOOP PRINCIPAL
# -------------------------
running = True

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # ---- MENÚ ----
        if state == STATE_MENU:
            action = menu.handle_event(event)
            if action == "play":
                reset_run()
                enemy_id = ENEMY_SEQUENCE[current_enemy_idx]
                game, renderer, input_handler = start_game(player_deck_ids, enemy_id)
                state = STATE_GAME
            elif action == "quit":
                running = False

        # ---- COMBATE ----
        elif state == STATE_GAME:
            if event.type == pygame.MOUSEBUTTONDOWN:
                input_handler.handle_click(pygame.mouse.get_pos())

        # ---- RECOMPENSA ----
        elif state == STATE_REWARD:
            action = reward.handle_event(event)
            if action == "confirm":
                # Añadir cartas elegidas al deck persistente
                for card in reward.get_chosen_cards():
                    cid = name_to_id.get(card.name)
                    if cid:
                        player_deck_ids.append(cid)
                        print(f"➕ {card.name} añadida al deck")

                reward = None
                current_enemy_idx += 1

                if current_enemy_idx < len(ENEMY_SEQUENCE):
                    # Siguiente combate
                    enemy_id = ENEMY_SEQUENCE[current_enemy_idx]
                    print(f"\n⚔️  Siguiente enemigo: {enemy_id}")
                    game, renderer, input_handler = start_game(player_deck_ids, enemy_id)
                    state = STATE_GAME
                else:
                    # Run completada — volver al menú y resetear
                    print("\n🏆 ¡Run completada!")
                    reset_run()
                    state = STATE_MENU

    # ---- UPDATE ----
    if state == STATE_MENU:
        menu.update(dt)

    elif state == STATE_GAME:
        game.delta_time = dt
        game.update(dt)

        # Victoria → pantalla de recompensa
        if game.game_over and game.enemy.hp <= 0:
            reward = RewardScreen(screen, game.enemy, factory)
            state  = STATE_REWARD

        # Derrota → volver al menú con el deck reseteado
        if game.game_over and game.player.hp <= 0:
            reset_run()
            state = STATE_MENU

        if input_handler.attack_mode:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif state == STATE_REWARD:
        reward.update(dt)

    # ---- DRAW ----
    if state == STATE_MENU:
        menu.draw()

    elif state == STATE_GAME:
        renderer.draw()

    elif state == STATE_REWARD:
        renderer.draw()   # tablero congelado de fondo
        reward.draw()     # overlay encima

    pygame.display.flip()

pygame.quit()

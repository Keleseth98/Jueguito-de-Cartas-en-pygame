import pygame
import random
from utils import constants as cs


class RewardScreen:
    """
    Pantalla post-combate: muestra 3 cartas aleatorias del deck del enemigo.
    El jugador puede seleccionar las que quiera (0 a 3) y confirmar.

    Uso desde main.py:
        reward = RewardScreen(screen, enemy, card_factory)
        # en el loop:
        action = reward.handle_event(event)   # "confirm" | None
        reward.update(dt)
        reward.draw()
        # cuando action == "confirm":
        chosen = reward.get_chosen_cards()    # lista de Card ya instanciadas
    """

    CARD_W = 150
    CARD_H = 210
    CARD_SPACING = 220

    def __init__(self, screen, enemy, card_factory):
        self.screen       = screen
        self.card_factory = card_factory

        self.font_title = pygame.font.Font(None, 64)
        self.font_sub   = pygame.font.Font(None, 32)
        self.font_btn   = pygame.font.Font(None, 38)
        self.font_card  = pygame.font.Font(None, 26)

        # Reconstruir ids únicos del deck del enemigo
        deck_ids = self._get_enemy_deck_ids(enemy)
        sample   = random.sample(deck_ids, min(3, len(deck_ids)))

        # Instanciar las cartas de recompensa
        self.reward_cards = [card_factory.create(cid) for cid in sample]
        self.selected     = set()

        # Layout: centrar las cartas
        n       = len(self.reward_cards)
        total_w = n * self.CARD_W + (n - 1) * (self.CARD_SPACING - self.CARD_W)
        start_x = cs.SCREEN_WIDTH  // 2 - total_w // 2
        card_y  = cs.SCREEN_HEIGHT // 2 - self.CARD_H // 2 - 20

        self.card_rects = []
        for i in range(n):
            x = start_x + i * self.CARD_SPACING
            self.card_rects.append(pygame.Rect(x, card_y, self.CARD_W, self.CARD_H))

        # Botón confirmar
        btn_w, btn_h = 220, 55
        self.btn_rect = pygame.Rect(
            cs.SCREEN_WIDTH // 2 - btn_w // 2,
            card_y + self.CARD_H + 60,
            btn_w, btn_h
        )

        # Fade-in
        self.alpha   = 0.0
        self.fade_in = True

        self._overlay = pygame.Surface((cs.SCREEN_WIDTH, cs.SCREEN_HEIGHT))
        self._overlay.fill((0, 0, 0))

    # --------------------------------------------------
    def _get_enemy_deck_ids(self, enemy):
        all_cards  = list(enemy.deck.cards) + list(enemy.hand) + list(enemy.discard)
        db_cards   = self.card_factory.db.cards
        name_to_id = {data["name"]: cid for cid, data in db_cards.items()}
        ids = []
        for card in all_cards:
            cid = name_to_id.get(card.name)
            if cid and cid not in ids:
                ids.append(cid)
        return ids if ids else list(db_cards.keys())

    # --------------------------------------------------
    def handle_event(self, event):
        if self.fade_in:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos

            for i, rect in enumerate(self.card_rects):
                if rect.collidepoint(pos):
                    if i in self.selected:
                        self.selected.discard(i)
                    else:
                        self.selected.add(i)
                    return None

            if self.btn_rect.collidepoint(pos):
                return "confirm"

        return None

    def update(self, dt):
        if self.fade_in:
            self.alpha = min(self.alpha + dt * 3, 1.0)
            if self.alpha >= 1.0:
                self.fade_in = False

    def get_chosen_cards(self):
        return [self.reward_cards[i] for i in sorted(self.selected)]

    def draw(self):
        self._overlay.set_alpha(int(200 * self.alpha))
        self.screen.blit(self._overlay, (0, 0))

        if self.alpha < 0.05:
            return

        # Título
        title = self.font_title.render("¡Victoria!", True, (255, 220, 60))
        self.screen.blit(title, (
            cs.SCREEN_WIDTH // 2 - title.get_width() // 2,
            self.card_rects[0].top - 130
        ))

        # Subtítulo
        sub = self.font_sub.render(
            "Elige las cartas que quieres añadir a tu deck  (0–3)",
            True, (180, 180, 180)
        )
        self.screen.blit(sub, (
            cs.SCREEN_WIDTH // 2 - sub.get_width() // 2,
            self.card_rects[0].top - 70
        ))

        # Cartas
        for i, (card, rect) in enumerate(zip(self.reward_cards, self.card_rects)):
            selected = i in self.selected

            if selected:
                glow = pygame.Rect(rect.x - 5, rect.y - 5, rect.w + 10, rect.h + 10)
                pygame.draw.rect(self.screen, (255, 220, 60), glow, border_radius=6)

            img = pygame.transform.smoothscale(card.image, (self.CARD_W, self.CARD_H))
            self.screen.blit(img, rect.topleft)

            border_color = (255, 220, 60) if selected else (100, 100, 100)
            pygame.draw.rect(self.screen, border_color, rect, 3, border_radius=4)

            # Nombre
            name_surf = self.font_card.render(card.name, True, (255, 255, 255))
            self.screen.blit(name_surf, (
                rect.centerx - name_surf.get_width() // 2,
                rect.bottom + 10
            ))

            # Stats (criatura)
            if hasattr(card, "attack") and hasattr(card, "health"):
                stats = self.font_card.render(
                    f"{card.attack} / {card.health}", True, (200, 200, 200)
                )
                self.screen.blit(stats, (
                    rect.centerx - stats.get_width() // 2,
                    rect.bottom + 32
                ))
            # Costo (hechizo)
            elif hasattr(card, "mana_cost"):
                cost = self.font_card.render(
                    f"Mana: {card.mana_cost}", True, (120, 180, 255)
                )
                self.screen.blit(cost, (
                    rect.centerx - cost.get_width() // 2,
                    rect.bottom + 32
                ))

            if selected:
                check = self.font_sub.render("✓", True, (255, 220, 60))
                self.screen.blit(check, (rect.right - 24, rect.top + 6))

        # Botón
        mx, my = pygame.mouse.get_pos()
        hovered   = self.btn_rect.collidepoint(mx, my)
        btn_color  = (60, 160, 60)  if hovered else (40, 120, 40)
        btn_border = (120, 255, 120) if hovered else (80, 180, 80)

        pygame.draw.rect(self.screen, btn_color,  self.btn_rect, border_radius=8)
        pygame.draw.rect(self.screen, btn_border, self.btn_rect, 2, border_radius=8)

        n     = len(self.selected)
        label = "Continuar" if n == 0 else f"Añadir {n} carta{'s' if n > 1 else ''}"
        btn_text = self.font_btn.render(label, True, (255, 255, 255))
        self.screen.blit(btn_text, (
            self.btn_rect.centerx - btn_text.get_width() // 2,
            self.btn_rect.centery - btn_text.get_height() // 2
        ))

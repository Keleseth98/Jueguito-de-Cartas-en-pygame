import pygame
from utils import constants as cs


class Button:
    def __init__(self, text, x, y, width=260, height=60):
        self.text = text
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.color_normal  = (40, 40, 40)
        self.color_hover   = (70, 70, 70)
        self.color_border  = (180, 180, 180)
        self.color_border_hover = (255, 255, 255)
        self.font = pygame.font.Font(None, 42)

    def draw(self, screen):
        mx, my = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mx, my)

        bg     = self.color_hover  if hovered else self.color_normal
        border = self.color_border_hover if hovered else self.color_border

        pygame.draw.rect(screen, bg, self.rect, border_radius=8)
        pygame.draw.rect(screen, border, self.rect, 2, border_radius=8)

        label = self.font.render(self.text, True, (255, 255, 255))
        lx = self.rect.centerx - label.get_width() // 2
        ly = self.rect.centery - label.get_height() // 2
        screen.blit(label, (lx, ly))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class MainMenu:
    """
    Devuelve la acción elegida:
      "play"  → iniciar partida
      "quit"  → cerrar el juego
      None    → seguir mostrando el menú
    """

    def __init__(self, screen):
        self.screen = screen
        self.cx = cs.SCREEN_WIDTH  // 2
        self.cy = cs.SCREEN_HEIGHT // 2

        # Fuentes
        self.font_title    = pygame.font.Font(None, 110)
        self.font_subtitle = pygame.font.Font(None, 36)

        # Botones centrados verticalmente
        self.btn_play = Button("Jugar",  self.cx, self.cy + 20)
        self.btn_quit = Button("Salir",  self.cx, self.cy + 110)

        # Animación del título (pulso suave)
        self.title_timer = 0.0

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = event.pos
            if self.btn_play.is_clicked(pos):
                return "play"
            if self.btn_quit.is_clicked(pos):
                return "quit"
        return None

    def update(self, dt):
        self.title_timer += dt

    def draw(self):
        self.screen.fill((10, 10, 10))

        # Línea decorativa superior
        pygame.draw.line(
            self.screen,
            (80, 80, 80),
            (self.cx - 300, self.cy - 130),
            (self.cx + 300, self.cy - 130),
            1
        )

        # Título con pulso de brillo muy sutil
        import math
        pulse = int(215 + 40 * math.sin(self.title_timer * 2))
        color_title = (pulse, pulse, pulse)

        title = self.font_title.render("Jueguito", True, color_title)
        self.screen.blit(
            title,
            (self.cx - title.get_width() // 2, self.cy - 210)
        )

        # Subtítulo
        sub = self.font_subtitle.render("de Cartas", True, (130, 130, 130))
        self.screen.blit(
            sub,
            (self.cx - sub.get_width() // 2, self.cy - 110)
        )

        # Línea decorativa inferior (bajo subtítulo)
        pygame.draw.line(
            self.screen,
            (80, 80, 80),
            (self.cx - 300, self.cy - 80),
            (self.cx + 300, self.cy - 80),
            1
        )

        # Botones
        self.btn_play.draw(self.screen)
        self.btn_quit.draw(self.screen)

        # Versión en esquina
        ver = pygame.font.Font(None, 24).render("v0.1", True, (50, 50, 50))
        self.screen.blit(ver, (cs.SCREEN_WIDTH - 50, cs.SCREEN_HEIGHT - 30))

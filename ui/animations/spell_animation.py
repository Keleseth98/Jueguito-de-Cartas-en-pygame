import pygame
from utils import constants as cs


class SpellAnimation:
    """
    Muestra la carta del hechizo en el centro de la pantalla:
    crece de tamaño y se vuelve transparente hasta desaparecer.

    Duración total: 1.2s
    """

    BASE_W = 150
    BASE_H = 210
    DURATION = 1.2

    def __init__(self, card):
        self.card     = card
        self.timer    = 0.0
        self.finished = False

        self.cx = cs.SCREEN_WIDTH  // 2
        self.cy = cs.SCREEN_HEIGHT // 2

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.DURATION:
            self.finished = True

    def draw(self, screen):
        if self.finished:
            return

        t = self.timer / self.DURATION   # 0.0 → 1.0

        # Escala: 1.0 → 2.5
        scale  = 1.0 + 1.5 * t
        width  = int(self.BASE_W * scale)
        height = int(self.BASE_H * scale)

        # Alpha: 255 → 0  (desaparece suavemente)
        alpha = int(255 * (1.0 - t))

        # Escalar imagen
        img = pygame.transform.smoothscale(self.card.image, (width, height))

        # Aplicar transparencia
        img.set_alpha(alpha)

        # Centrar en pantalla
        x = self.cx - width  // 2
        y = self.cy - height // 2

        screen.blit(img, (x, y))

        # Nombre del hechizo, también con fade
        font  = pygame.font.Font(None, 42)
        label = font.render(self.card.name, True, (255, 220, 100))
        label.set_alpha(alpha)
        screen.blit(label, (
            self.cx - label.get_width()  // 2,
            y - 40
        ))

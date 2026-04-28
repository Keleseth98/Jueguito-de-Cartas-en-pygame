import pygame

class DamageText:
    def __init__(self, value, x, y):
        self.value = value

        # posición base
        self.x = x
        self.y = y

        # animación
        self.time = 0
        self.duration = 0.3

        self.start_y = y + 40   # empieza abajo
        self.end_y = y - 60     # sube

        self.scale = 0.5
        self.max_scale = 2.0

        self.alpha = 255

        self.font = pygame.font.Font(None, 60)

    def update(self, dt):
        self.time += dt
        t = self.time / self.duration

        if t > 1:
            return False  # destruir

        # interpolación vertical (sube)
        self.y = self.start_y + (self.end_y - self.start_y) * t

        # escala (crece)
        self.scale = 0.5 + (self.max_scale - 0.5) * t

        # fade out
        self.alpha = 255 * (1 - t)

        return True

    def draw(self, screen):
        text = self.font.render(str(self.value), True, (255, 50, 50))

        # escalar
        size = text.get_size()
        text = pygame.transform.smoothscale(
            text,
            (int(size[0] * self.scale), int(size[1] * self.scale))
        )

        text.set_alpha(int(self.alpha))

        screen.blit(text, (self.x, self.y))
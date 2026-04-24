import pygame

class Card:
    def __init__(self, name, image_path):
        self.name = name
        self.image_path = image_path

        # IMAGEN
        img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.smoothscale(img, (150, 210))

        # POSICIÓN BASE (lógica)
        self.base_x = 0
        self.base_y = 0

        # POSICIÓN RENDER (animaciones)
        self.render_x = 0
        self.render_y = 0

        # ESCALA (hover, animaciones)
        self.scale = 1.0

        # HITBOX
        self.rect = None

        # ESTADOS
        self.hovered = False

    def update_rect(self):
        import pygame
        self.rect = pygame.Rect(
            self.render_x,
            self.render_y,
            int(150 * self.scale),
            int(210 * self.scale)
        )

    def play(self, source, target, context):
        raise NotImplementedError("Cada carta debe implementar play()")
import pygame
from ui.animations.damage_text import DamageText

class CombatAnimation:
    def __init__(self, attacker, defender):
        self.attacker = attacker
        self.defender = defender
        self.damage_texts = []
        self.damage_triggered = False

        self.timer = 0
        self.duration = 1.5  # total animación

        self.phase = "impact"  
        # impact (1s) → result (0.5s)

        self.finished = False

    def update(self, dt):
        self.timer += dt

        # MOMENTO DEL IMPACTO (0.5s)
        if not self.damage_triggered and self.timer >= 0.5:
            self.damage_triggered = True

            # daño al defensor
            self.damage_texts.append(
                DamageText(self.attacker.attack, 1200, 450)
            )

            # daño al atacante (si aplica)
            if hasattr(self.defender, "attack"):
                self.damage_texts.append(
                    DamageText(self.defender.attack, 250, 450)
                )

        # actualizar textos
        self.damage_texts = [
            dtxt for dtxt in self.damage_texts if dtxt.update(dt)
        ]

        #  cambio de fase visual
        if self.timer >= 1.0 and self.phase == "impact":
            self.phase = "result"

        #  terminar animación
        if self.timer >= self.duration:
            self.finished = True

    def draw(self, screen):
        #  posiciones
        left_pos = (300, 200)
        right_pos = (900, 200)

        # imágenes grandes (usa original)
        attacker_img = pygame.transform.smoothscale(
            self.attacker.original_image, (300, 420)
        )

        defender_img = pygame.transform.smoothscale(
            self.defender.original_image, (300, 420)
        )

        #  dibujar
        screen.blit(attacker_img, left_pos)
        screen.blit(defender_img, right_pos)

        # dibujar textos de daño
        for dtxt in self.damage_texts:
            dtxt.draw(screen)

        # overlay de daño
        if self.phase == "impact":
            # defensor rojo fuerte
            red_overlay = pygame.Surface((300, 420), pygame.SRCALPHA)
            red_overlay.fill((255, 0, 0, 120))
            screen.blit(red_overlay, right_pos)



        elif self.phase == "result":
            # 🔥 si alguien murió
            if not self.defender.is_alive():
                red = pygame.Surface((300, 420), pygame.SRCALPHA)
                red.fill((255, 0, 0, 180))
                screen.blit(red, right_pos)

            if not self.attacker.is_alive():
                red = pygame.Surface((300, 420), pygame.SRCALPHA)
                red.fill((255, 0, 0, 180))
                screen.blit(red, left_pos)
import pygame
import os

class PowerUp:
    def __init__(self, x, y, width=90, height=60):
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False

        # Försök ladda hatt-sprite
        base_path = os.path.dirname(__file__)
        hat_path = os.path.join(base_path, "..", "assets", "sprites", "hatt.png")

        self.use_sprite = False
        self.sprite = None

        if os.path.exists(hat_path):
            try:
                image = pygame.image.load(hat_path).convert_alpha()
                self.sprite = pygame.transform.scale(image, (width, height))
                self.use_sprite = True
            except Exception as e:
                print("Failed to load hat sprite:", e)

    def draw(self, screen):
        if self.collected:
            return

        if self.use_sprite:
            screen.blit(self.sprite, self.rect)
        else:
            # fallback – borde aldrig synas
            pygame.draw.rect(screen, (139, 69, 19), self.rect)

    def check_collision(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return True
        return False

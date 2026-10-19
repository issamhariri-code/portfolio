import pygame
import os


class Collectible:
    """
    Collectible items (mushrooms) that players can pick up.
    Uses placeholder graphic until actual sprite is available.
    """
    def __init__(self, x, y, width=40, height=40):
        """
        Initialize a collectible item.

        Args:
            x: X position
            y: Y position
            width: Width of collectible (default 40)
            height: Height of collectible (default 40)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False

        # Placeholder visual (yellow circle with brown outline for mushroom)
        # This will be replaced with actual sprite later
        self.placeholder_color = (255, 215, 0)  # Gold/yellow
        self.outline_color = (139, 69, 19)      # Brown

        # Try to load sprite if available, otherwise use placeholder
        self.use_sprite = False
        base_path = os.path.dirname(__file__)
        sprite_path = os.path.join(base_path, "..", "assets", "tilesets", "mashroom.png")

        if os.path.exists(sprite_path):
            try:
                self.sprite = pygame.image.load(sprite_path).convert_alpha()
                self.sprite = pygame.transform.scale(self.sprite, (width, height))
                self.use_sprite = True
            except:
                self.use_sprite = False

    def draw(self, screen):
        """Draw the collectible if not collected."""
        if not self.collected:
            if self.use_sprite:
                screen.blit(self.sprite, self.rect)
            else:
                # Draw placeholder: circle with outline
                center = self.rect.center
                radius = min(self.rect.width, self.rect.height) // 2
                pygame.draw.circle(screen, self.outline_color, center, radius)
                pygame.draw.circle(screen, self.placeholder_color, center, radius - 2)

    def check_collision(self, player_rect):
        """
        Check if player collides with this collectible.

        Args:
            player_rect: The player's pygame.Rect

        Returns:
            True if collected, False otherwise
        """
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return True
        return False

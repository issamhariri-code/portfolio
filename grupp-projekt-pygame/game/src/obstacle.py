import pygame
import os

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, sprite_name="treeplatform"):
        super().__init__()

        # Try to load platform image (default: tree, Level 2: cloud)
        base_path = os.path.dirname(__file__)

        # Check for cloud sprite first (Level 2), then tree sprite (Level 1), then fallback
        # FIXED: Prioritize tilesets directory where cloud.png actually is
        possible_paths = [
            os.path.join(base_path, "..", "assets", "tilesets", f"{sprite_name}.png"),
            os.path.join(base_path, "..", "assets", "maps", "level2", f"{sprite_name}.png"),  # Fallback
        ]

        image_loaded = False
        for platform_image_path in possible_paths:
            if os.path.exists(platform_image_path):
                try:
                    # Load and scale the platform image
                    original_image = pygame.image.load(platform_image_path).convert_alpha()
                    self.image = pygame.transform.scale(original_image, (width, height))
                    image_loaded = True
                    break
                except:
                    continue

        if not image_loaded:
            # Fallback to dark wood texture if image not found
            self.image = pygame.Surface((width, height))

            # Dark wood colors - rich brown tones
            dark_wood = (60, 40, 20)      # Very dark brown base
            wood_grain = (80, 50, 25)     # Slightly lighter brown
            wood_highlight = (100, 65, 35) # Lighter wood grain
            wood_border = (40, 25, 10)    # Almost black border

            # Fill base with dark wood color
            self.image.fill(dark_wood)

            # Add wood grain texture with horizontal lines
            for i in range(0, height, 4):
                # Alternate between grain colors for texture
                if i % 8 == 0:
                    pygame.draw.line(self.image, wood_grain, (0, i), (width, i), 2)
                elif i % 6 == 0:
                    pygame.draw.line(self.image, wood_highlight, (0, i), (width, i), 1)

            # Add some vertical variation for more realistic wood grain
            for i in range(0, width, 20):
                pygame.draw.line(self.image, wood_grain, (i, 0), (i, height), 1)

            # Draw dark border around platform (wood edge)
            pygame.draw.rect(self.image, wood_border, (0, 0, width, height), 2)

            # Add top highlight to give depth
            pygame.draw.line(self.image, wood_highlight, (2, 2), (width-2, 2), 1)

        # Hitbox matches full image size (user edited image resolution)
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, screen):
        screen.blit(self.image, self.rect)
import pygame
import random
import math
import os


class FlyingEnemy(pygame.sprite.Sprite):
    """
    Flying enemy that moves in wave patterns and actively chases player.
    Poses a real threat in Level 2 with intelligent chase behavior.
    """
    def __init__(self, x, y):
        super().__init__()

        # ändra: ladda bläckfisk-sprite istället för röd ruta
        self.size = 60  # storlek för bläckfisken
        
        # ladda octopus.png
        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "..", "assets", "sprites", "enemies", "octopus.png")
        
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except pygame.error:
            # fallback till röd ruta om bilden inte hittas
            print(f"Warning: Could not load {image_path}, using red square")
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((255, 0, 0))
            pygame.draw.rect(self.image, (255, 255, 255), (0, 0, self.size, self.size), 3)
        
        self.rect = self.image.get_rect(center=(x, y))

        # Movement
        self.speed = 1.0  # Reduced speed for better balance
        self.wave_amplitude = 20  # Reduced wave height for more predictable movement
        self.wave_frequency = 0.02  # Slower wave oscillation
        self.wave_offset = random.uniform(0, 2 * math.pi)

        # Chase behavior
        self.chase_range = 250  # Reduced chase range to be less aggressive
        self.base_x = x
        self.base_y = y
        self.time = 0


    def update(self, player, screen_width, screen_height):
        """
        Update flying enemy position and behavior.

        Args:
            player: The player object to chase
            screen_width: Width of the screen for wrapping
            screen_height: Height of the screen for boundary checks
        """
        self.time += 1

        # Calculate distance to player
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        if distance < self.chase_range and distance > 0:
            # Chase player
            direction_x = dx / distance
            direction_y = dy / distance

            self.rect.x += direction_x * self.speed
            self.rect.y += direction_y * self.speed

            # Add wave motion while chasing (makes movement unpredictable)
            wave_offset = math.sin(self.time * self.wave_frequency + self.wave_offset) * 15
            self.rect.y += wave_offset
        else:
            # Patrol in wave pattern
            self.rect.x += self.speed
            wave_y = math.sin(self.time * self.wave_frequency + self.wave_offset) * self.wave_amplitude
            self.rect.y = self.base_y + wave_y

        # Wrap around screen edges
        if self.rect.left > screen_width:
            self.rect.right = 0
            self.base_y = random.randint(200, screen_height - 200)
        elif self.rect.right < 0:
            self.rect.left = screen_width
            self.base_y = random.randint(200, screen_height - 200)

    def draw(self, screen):
        """Draw the flying enemy."""
        screen.blit(self.image, self.rect)

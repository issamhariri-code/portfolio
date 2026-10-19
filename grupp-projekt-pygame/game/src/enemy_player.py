import pygame
import os
import random

class EnemyPlayer(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, image_dir):
        super().__init__()
        
        self.width = 80
        self.height = 100
        
        # Försök ladda enemy-bild, annars skapa röd rektangel
        enemy_path = os.path.join(image_dir, "enemy.png")
        try:
            self.image = pygame.transform.scale(
                pygame.image.load(enemy_path).convert_alpha(),
                (self.width, self.height)
            )
            print("Enemy-bild laddad!")
        except:
            # Skapa röd rektangel som placeholder
            self.image = pygame.Surface((self.width, self.height))
            self.image.fill((255, 0, 0))  # Röd färg
            print(f"Varning: enemy.png saknas, skapar röd rektangel")

        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y

        # Random horizontal movement only (no vertical to avoid buggy appearance)
        self.speed_x = random.choice([-2, -1, 1, 2])  # Random horisontell hastighet (reduced speed)
        self.speed_y = 0  # No vertical movement - stays at spawn height

        # Timer för att ändra riktning ibland
        self.direction_timer = 0
        self.direction_change_interval = random.randint(180, 300)  # Byt riktning var 3-5 sekund (slower changes)

    def update(self, obstacles=None, screen_width=1920, screen_height=600):
        # Horizontal movement only
        self.rect.x += self.speed_x

        # Loopa runt när fienden når kanterna (X-axel)
        if self.rect.left > screen_width:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = screen_width

        # Ändra riktning slumpmässigt ibland
        self.direction_timer += 1
        if self.direction_timer >= self.direction_change_interval:
            self.speed_x = random.choice([-2, -1, 1, 2])
            self.direction_timer = 0
            self.direction_change_interval = random.randint(180, 300)

    def draw(self, screen): 
        """Rita fienden på skärmen"""
        screen.blit(self.image, self.rect) # Rita fienden på skärmen
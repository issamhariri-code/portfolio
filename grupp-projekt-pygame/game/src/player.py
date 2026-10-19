import pygame
import os

# Konstanter (EXAKT som test.py lines 22-24)
GRAVITY = 0.8
JUMP_STRENGTH = -20
MOVE_SPEED = 5

class Player:
    """
    spelarklassen hanterar spelarens position, rörelse och kollisioner.
    använder EXAKT samma fysik och kontrollsystem som test.py.
    """
    def __init__(self, start_x, start_y, max_jumps=1):
        # spelarens dimensioner och färg.
        self.width = 80
        self.height = 100
        self.collision_height = 75  # ÄNDRAT: Höjd ökad från 70 till 75
        self.collision_width = 10  # ÄNDRAT: Bredare kollisionsbox för bättre visuell-fysisk matchning
        self.visual_offset = 25  # ÄNDRAT: Mindre offset (från 30 till 25)
        self.color = (50, 120, 200)

        # Jump system - level-based (Level 1: 1 jump, Level 2: 2 jumps)
        self.max_jumps = max_jumps

        # ladda alla sprite-bilder
        base_path = os.path.dirname(__file__)
        sprites_dir = os.path.join(base_path, "..", "assets", "sprites", "pepe")
        normal_dir = os.path.join(sprites_dir, "normal")
        hat_dir = os.path.join(sprites_dir, "with_hat")

        # idle (stilla)
        idle_path = os.path.join(normal_dir, "pepe.png")
        self.image_idle = pygame.transform.scale(
            pygame.image.load(idle_path).convert_alpha(),
            (self.width, self.height)
        )

        # pendlar med armarna, går framåt
        walk1_path = os.path.join(normal_dir, "pepe_walk1.png")
        self.image_walk1 = pygame.transform.scale(
            pygame.image.load(walk1_path).convert_alpha(),
            (self.width, self.height)
        )
        self.image_walk1.set_colorkey((255, 255, 255))
        
        # pendling armar motsatt håll
        walk2_path = os.path.join(normal_dir, "pepe_walk2.png")
        self.image_walk2 = pygame.transform.scale(
            pygame.image.load(walk2_path).convert_alpha(),
            (self.width, self.height)
        )
        self.image_walk2.set_colorkey((255, 255, 255))

        # hopp
        jump_path = os.path.join(normal_dir, "pepe_jump.png")
        self.image_jump = pygame.transform.scale(
            pygame.image.load(jump_path).convert_alpha(),
            (self.width, self.height)
        )
        self.image_jump.set_colorkey((255, 255, 255))

        # duck (ducka)
        duck_path = os.path.join(normal_dir, "pepe_duck.png")
        self.image_duck = pygame.transform.scale(
            pygame.image.load(duck_path).convert_alpha(),
            (self.width, self.height // 2)
        )
        self.image_duck.set_colorkey((255, 255, 255))

        # Hat variants (for fedora power-up)
        # Use EXACT same dimensions as non-hat sprites
        SPRITE_WIDTH = self.width  # 80
        SPRITE_HEIGHT = self.height  # 100

        standing_hat_path = os.path.join(hat_dir, "standing_hat.png")
        self.image_idle_hat = pygame.transform.scale(
            pygame.image.load(standing_hat_path).convert_alpha(),
            (SPRITE_WIDTH, SPRITE_HEIGHT)  # EXACT same as idle
        )

        walk1_hat_path = os.path.join(hat_dir, "walk1_hat.png")
        self.image_walk1_hat = pygame.transform.scale(
            pygame.image.load(walk1_hat_path).convert_alpha(),
            (SPRITE_WIDTH, SPRITE_HEIGHT)  # EXACT same as walk1
        )
        self.image_walk1_hat.set_colorkey((255, 255, 255))

        walk2_hat_path = os.path.join(hat_dir, "walk2_hat.png")
        self.image_walk2_hat = pygame.transform.scale(
            pygame.image.load(walk2_hat_path).convert_alpha(),
            (SPRITE_WIDTH, SPRITE_HEIGHT)  # EXACT same as walk2
        )
        self.image_walk2_hat.set_colorkey((255, 255, 255))

        jump_hat_path = os.path.join(hat_dir, "jump_hat.png")
        self.image_jump_hat = pygame.transform.scale(
            pygame.image.load(jump_hat_path).convert_alpha(),
            (SPRITE_WIDTH, SPRITE_HEIGHT)  # EXACT same as jump
        )
        self.image_jump_hat.set_colorkey((255, 255, 255))

        duck_hat_path = os.path.join(hat_dir, "duck_hat.png")
        self.image_duck_hat = pygame.transform.scale(
            pygame.image.load(duck_hat_path).convert_alpha(),
            (SPRITE_WIDTH, SPRITE_HEIGHT // 2)  # EXACT same as duck
        )
        self.image_duck_hat.set_colorkey((255, 255, 255))

        # Pre-flip alla bilder en gång (ökad fps från main branch)
        self.image_idle_flipped = pygame.transform.flip(self.image_idle, True, False)
        self.image_walk1_flipped = pygame.transform.flip(self.image_walk1, True, False)
        self.image_walk2_flipped = pygame.transform.flip(self.image_walk2, True, False)
        self.image_jump_flipped = pygame.transform.flip(self.image_jump, True, False)
        self.image_duck_flipped = pygame.transform.flip(self.image_duck, True, False)

        # börja med idle som aktuell bild
        self.current_image = self.image_idle

        # timer för att växla mellan gång animationerna
        self.animation_timer = 0
        self.animation_speed = 10
        self.walk_frame = 1

        # håll koll på riktning
        self.facing_left = False
        
        # skapa pygame rect för position - använd bottom för korrekt plattformskontakt
        # Centrera den smala kollisionsboxen
        self.rect = pygame.Rect(start_x, 0, self.collision_width, self.collision_height)
        self.rect.bottom = start_y

        # hastighets-variabler
        self.vel_x = 0
        self.vel_y = 0
        self.on_ground = False
        self.is_ducking = False
        self.jumps_left = max_jumps  # Initialize from level-based max_jumps parameter
        self.has_hat = False  # Fedora power-up status

    @property
    def x(self):
        """getter för x-position (för BackgroundManager kompatibilitet)"""
        return self.rect.x

    @x.setter
    def x(self, value):
        """setter för x-position (för BackgroundManager kompatibilitet)"""
        self.rect.x = value

    def draw(self, screen):
        """rita spelaren på skärmen med aktuell sprite"""
        image_rect = self.current_image.get_rect()
        image_rect.centerx = self.rect.centerx
        image_rect.bottom = self.rect.bottom + self.visual_offset  # LÄGG TILLBAKA + self.visual_offset
        screen.blit(self.current_image, image_rect)

    def jump(self):
        """hoppa om spelaren är på marken eller har hopp kvar"""
        if self.jumps_left > 0:
            self.vel_y = JUMP_STRENGTH
            self.jumps_left -= 1

    def check_collision_x(self, platforms):
        """kollisionskontroll X-axeln (horisontell)"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_x > 0:
                    self.rect.right = platform.rect.left
                elif self.vel_x < 0:
                    self.rect.left = platform.rect.right

    def check_collision_y(self, platforms):
        """kollisionskontroll Y-axeln (vertikal)"""
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumps_left = self.max_jumps  # Reset to level-based max jumps
                elif self.vel_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

    def update(self, obstacles, screen_width=800, screen_height=600):
        """uppdatera spelarens position och hantera kollisioner"""
        # hantera input för vänster/höger rörelse
        keys = pygame.key.get_pressed()
        
        # spara föregående riktning
        prev_vel_x = self.vel_x
        self.vel_x = 0
        
        # håll koll på vilken riktning spelaren går
        moving_left = False
        moving_right = False

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -MOVE_SPEED
            moving_left = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = MOVE_SPEED
            moving_right = True

        # resetta animation om riktning ändras eller spelaren stannar
        if (prev_vel_x > 0 and self.vel_x < 0) or (prev_vel_x < 0 and self.vel_x > 0) or (prev_vel_x != 0 and self.vel_x == 0):
            self.animation_timer = 0
            self.walk_frame = 1

        # applicera gravity
        self.vel_y += GRAVITY

        # uppdatera horisontell position
        self.rect.x += self.vel_x
        self.check_collision_x(obstacles)

        # uppdatera vertikal position
        self.rect.y += self.vel_y
        self.on_ground = False
        self.check_collision_y(obstacles)

        # extra kontroll - säkerställ exakt landing på plattformar
        if self.vel_y >= 0:  # bara när vi faller nedåt
            for platform in obstacles:
                # kolla om spelarens botten är nära plattformens topp
                if (self.rect.colliderect(platform.rect) and
                    self.rect.bottom >= platform.rect.top and
                    self.rect.top < platform.rect.top):
                    # snap till exakt position
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                    self.jumps_left = self.max_jumps
                    break
        

        

        # håll spelaren inom skärmgränserna
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

        # uppdatera sprite baserat på rörelse
        # UPPDATERA: facing direction FÖRST
        if moving_left:
            self.facing_left = True
        elif moving_right:
            self.facing_left = False
        
        # kolla om spelaren duckar
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            if not self.is_ducking:  # Bara första gången
                self.is_ducking = True
                old_bottom = self.rect.bottom
                self.rect.height = self.collision_height // 2
                self.rect.bottom = old_bottom
        else:
            # återställ normal höjd
            if self.is_ducking:
                old_bottom = self.rect.bottom
                self.rect.height = self.collision_height  # ÄNDRAT: Använd collision_height
                self.rect.bottom = old_bottom
                self.is_ducking = False
                
        if self.is_ducking:
            # visa duck-animation (skala ned bilden) - supports hat
            base_duck = self.image_duck_hat if self.has_hat else self.image_duck
            duck_image = pygame.transform.scale(base_duck, (self.width, self.rect.height))
            self.current_image = duck_image
            if moving_left:
                self.current_image = pygame.transform.flip(self.current_image, True, False)
        elif not self.on_ground:
            # Use hat variant if player has hat, otherwise normal with pre-flipped optimization
            if self.has_hat:
                self.current_image = self.image_jump_hat
                if self.facing_left:
                    self.current_image = pygame.transform.flip(self.current_image, True, False)
            else:
                self.current_image = self.image_jump_flipped if self.facing_left else self.image_jump
        elif self.vel_x != 0:
            # växla mellan walk1 och walk2 när spelaren går
            self.animation_timer += 1
            if self.animation_timer >= self.animation_speed:
                self.animation_timer = 0
                self.walk_frame = 2 if self.walk_frame == 1 else 1

            if self.walk_frame == 1:
                if self.has_hat:
                    self.current_image = self.image_walk1_hat
                    if self.facing_left:
                        self.current_image = pygame.transform.flip(self.current_image, True, False)
                else:
                    self.current_image = self.image_walk1_flipped if self.facing_left else self.image_walk1
            else:
                if self.has_hat:
                    self.current_image = self.image_walk2_hat
                    if self.facing_left:
                        self.current_image = pygame.transform.flip(self.current_image, True, False)
                else:
                    self.current_image = self.image_walk2_flipped if self.facing_left else self.image_walk2
        else:
            if self.has_hat:
                self.current_image = self.image_idle_hat
                if self.facing_left:
                    self.current_image = pygame.transform.flip(self.current_image, True, False)
            else:
                self.current_image = self.image_idle_flipped if self.facing_left else self.image_idle

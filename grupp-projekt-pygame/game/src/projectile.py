import pygame
import math
import random
import os

# NO GLOBAL LOADING - Load in each class to ensure pygame is ready

class Hitbox:
    """Basklass för alla boss-attacker och projektiler"""
    def __init__(self, x, y, width, height, damage=1, color=(255, 0, 0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.damage = damage
        self.color = color
        self.active = True
        self.lifetime = 0  # Frames aktiv
        self.warning = False  # Om hitboxen är i varningsfas

    def update(self):
        """Uppdatera livstid"""
        self.lifetime += 1

    def draw(self, screen):
        """Rita hitbox (enkla färgade rektanglar)"""
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)

    def check_collision(self, player_rect):
        """Kolla kollision med spelaren"""
        if self.active and not self.warning and self.rect.colliderect(player_rect):
            self.active = False
            return True
        return False


class TentacleSlam(Hitbox):
    """
    Tentakelslag - rektangel som faller från toppen
    Shadow phase: 90 frames (1.5 sekunder) - varning
    Attack phase: 60 frames (1 sekund) - attack faller
    """
    def __init__(self, x, y, screen_shake_callback=None):
        super().__init__(x, y, 200, 150, damage=1, color=(128, 0, 128))
        self.warning_duration = 90  # 1.5 sekunder varning
        self.attack_duration = 60   # 1 sekund attack
        self.warning = True
        self.start_y = -100  # Startar ovanför skärmen
        self.target_y = y    # Golv-position
        self.shadow_y = y    # Skugga på golvet
        self.falling = False
        self.has_hit_ground = False
        self.screen_shake_callback = screen_shake_callback

        # Load boss_crate.png directly - NO FALLBACKS
        base_dir = os.path.dirname(__file__)
        crate_path = os.path.join(base_dir, "..", "assets", "tilesets", "boss_crate.png")
        try:
            crate_img = pygame.image.load(crate_path).convert_alpha()
            self.crate_image = pygame.transform.scale(crate_img, (self.rect.width, self.rect.height))
            # Create faded version for warning
            self.crate_image_faded = self.crate_image.copy()
            self.crate_image_faded.set_alpha(128)
        except pygame.error as e:
            print(f"ERROR: Failed to load boss_crate.png for TentacleSlam attack!")
            print(f"Path attempted: {crate_path}")
            print(f"Pygame error: {e}")
            raise

    def update(self):
        """Uppdatera tentakelslag"""
        self.lifetime += 1

        # Varningsfas - visa skugga
        if self.lifetime < self.warning_duration:
            self.warning = True

        # Attack-fas - tentakel faller
        elif self.lifetime < self.warning_duration + self.attack_duration:
            self.warning = False
            self.falling = True

            # Flytta tentakel nedåt
            progress = (self.lifetime - self.warning_duration) / self.attack_duration
            self.rect.y = self.start_y + (self.target_y - self.start_y) * progress

            # Kolla om tentakel når golvet
            if self.rect.y >= self.target_y and not self.has_hit_ground:
                self.has_hit_ground = True
                # Trigga screen shake
                if self.screen_shake_callback:
                    self.screen_shake_callback()
        else:
            # Attack klar
            self.active = False

    def draw(self, screen):
        """Rita tentakelslag med boss_crate.png"""
        if not self.active:
            return

        if self.warning:
            # Warning: Faded boss crate at ground position
            screen.blit(self.crate_image_faded, (self.rect.x, self.shadow_y))
        else:
            # Attack: Full opacity boss crate falling
            screen.blit(self.crate_image, self.rect)


class EyeBeam(Hitbox):
    """
    Ögonstråle - vertikal linje som siktar sedan avfyrar
    Warning phase: 120 frames (2 sekunder) - tunn linje
    Attack phase: 60 frames (1 sekund) - tjock stråle
    """
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, damage=0, color=(0, 255, 255))  # Reducerad damage till 0
        self.warning_duration = 120  # 2 sekunder varning
        self.attack_duration = 60    # 1 sekund attack
        self.warning = True
        self.warning_width = 5       # Tunn linje för varning
        self.attack_width = width    # Tjock stråle för attack

        # Load laser-beams.png directly - NO FALLBACKS
        base_dir = os.path.dirname(__file__)
        laser_path = os.path.join(base_dir, "..", "assets", "tilesets", "laser-beams.png")
        try:
            laser_img = pygame.image.load(laser_path).convert_alpha()
            # Scale to match beam dimensions
            self.laser_image = pygame.transform.scale(laser_img, (self.rect.width, self.rect.height))
            # Create faded version for warning
            self.laser_image_faded = self.laser_image.copy()
            self.laser_image_faded.set_alpha(128)
        except pygame.error as e:
            print(f"ERROR: Failed to load laser-beams.png for EyeBeam attack!")
            print(f"Path attempted: {laser_path}")
            print(f"Pygame error: {e}")
            raise

    def update(self):
        """Uppdatera ögonstråle"""
        self.lifetime += 1

        # Varningsfas
        if self.lifetime < self.warning_duration:
            self.warning = True

        # Attack-fas
        elif self.lifetime < self.warning_duration + self.attack_duration:
            self.warning = False
        else:
            # Attack klar
            self.active = False

    def draw(self, screen):
        """Rita ögonstråle med laser beam sprite"""
        if not self.active:
            return

        if self.warning:
            # Warning: Faded laser beam
            screen.blit(self.laser_image_faded, self.rect)
        else:
            # Attack: Full opacity laser beam
            screen.blit(self.laser_image, self.rect)


class ProjectileShot(Hitbox):
    """
    Projektil - cirkel som rör sig nedåt
    Rör sig långsamt nedåt tills den når golvet eller träffar spelaren
    """
    def __init__(self, x, y, radius=25, vel_y=5):
        super().__init__(x - radius, y - radius, radius * 2, radius * 2, damage=1, color=(255, 100, 100))
        self.radius = radius
        self.vel_y = vel_y
        self.center_x = x
        self.center_y = y

        # Load fireorb.png directly - NO FALLBACKS
        base_dir = os.path.dirname(__file__)
        fireorb_path = os.path.join(base_dir, "..", "assets", "tilesets", "fireorb.png")
        try:
            fireorb_img = pygame.image.load(fireorb_path).convert_alpha()
            self.fireorb_image = pygame.transform.scale(fireorb_img, (self.rect.width, self.rect.height))
        except pygame.error as e:
            print(f"ERROR: Failed to load fireorb.png for ProjectileShot attack!")
            print(f"Path attempted: {fireorb_path}")
            print(f"Pygame error: {e}")
            raise

    def update(self):
        """Uppdatera projektil"""
        self.lifetime += 1

        # Rör sig nedåt
        self.center_y += self.vel_y
        self.rect.y += self.vel_y

        # Inaktivera om den går utanför skärmen
        if self.center_y > 1080:
            self.active = False

    def draw(self, screen):
        """Rita projektil med fireorb sprite"""
        if self.active:
            screen.blit(self.fireorb_image, self.rect)


class GravityPull(Hitbox):
    """
    Gravitationsdragning - punkt som drar spelaren mot sig
    Active: 180 frames (3 sekunder)
    Drar spelaren mot centrum, skadar om spelaren når centrum
    """
    def __init__(self, x, y, pull_radius=200, pull_strength=0.5):
        super().__init__(x - 20, y - 20, 40, 40, damage=1, color=(255, 0, 255))
        self.center_x = x
        self.center_y = y
        self.pull_radius = pull_radius  # Område där dragning påverkar
        self.pull_strength = pull_strength
        self.duration = 180  # 3 sekunder aktiv
        self.warning = True

    def update(self):
        """Uppdatera gravitationsdragning"""
        self.lifetime += 1

        # Första 30 frames är varning
        if self.lifetime > 30:
            self.warning = False

        # Inaktivera efter duration
        if self.lifetime > self.duration:
            self.active = False

    def apply_pull(self, player):
        """
        Applicera dragningskraft på spelaren
        Returns: (pull_x, pull_y) - kraft att applicera på spelaren
        """
        if not self.active or self.warning:
            return (0, 0)

        # Beräkna distans till centrum
        dx = self.center_x - player.rect.centerx
        dy = self.center_y - player.rect.centery
        distance = math.sqrt(dx * dx + dy * dy)

        # Ingen dragning om utanför radius
        if distance > self.pull_radius:
            return (0, 0)

        # Beräkna normalized direction
        if distance > 0:
            dir_x = dx / distance
            dir_y = dy / distance
        else:
            return (0, 0)

        # Starkare dragning ju närmare centrum
        strength = self.pull_strength * (1 - distance / self.pull_radius)

        return (dir_x * strength * 10, dir_y * strength * 10)

    def draw(self, screen):
        """Rita gravitationsdragning"""
        if not self.active:
            return

        if self.warning:
            # Rita varnings-cirkel (pulserar)
            # TODO: Replace with gravity pull warning sprite (pulsing vortex warning)
            pulse = int(50 + 20 * math.sin(self.lifetime * 0.2))
            pygame.draw.circle(screen, (255, 255, 0), (int(self.center_x), int(self.center_y)), pulse, 3)
        else:
            # Rita dragnings-effekt (concentriska cirklar)
            # TODO: Replace with gravity pull effect sprite (swirling vortex animation)
            for i in range(3):
                radius = int(self.pull_radius * (1 - i * 0.3))
                alpha = int(100 * (1 - i * 0.3))
                # Rita cirkel
                pygame.draw.circle(screen, self.color, (int(self.center_x), int(self.center_y)), radius, 2)

            # Rita centrum (damage zone)
            # TODO: Replace with vortex center sprite (danger zone)
            pygame.draw.circle(screen, (255, 0, 0), (int(self.center_x), int(self.center_y)), 20)


class FastSweep(Hitbox):
    """
    Snabb svepning - horisontell rektangel som rör sig över golvet
    Warning: 60 frames (1 sekund)
    Sweep: 90 frames (1.5 sekunder) - rör sig från vänster till höger
    """
    def __init__(self, y=980, direction=1):
        width = 160
        height = 120
        start_x = -width if direction > 0 else 1920
        super().__init__(start_x, y, width, height, damage=1, color=(255, 165, 0))
        self.warning_duration = 60
        self.sweep_duration = 90
        self.direction = direction  # 1 = höger, -1 = vänster
        self.speed = 25 if direction > 0 else -25
        self.warning = True
        self.warning_x = 0 if direction > 0 else 1840  # Varningstecken på sidan

        # Load ufo.png directly - NO FALLBACKS
        base_dir = os.path.dirname(__file__)
        ufo_path = os.path.join(base_dir, "..", "assets", "tilesets", "ufo.png")
        try:
            self.ufo_image_original = pygame.image.load(ufo_path).convert_alpha()
            self.ufo_image_sweep = pygame.transform.scale(self.ufo_image_original, (self.rect.width, self.rect.height))
        except pygame.error as e:
            print(f"ERROR: Failed to load ufo.png for FastSweep attack!")
            print(f"Path attempted: {ufo_path}")
            print(f"Pygame error: {e}")
            raise

    def update(self):
        """Uppdatera snabb svepning"""
        self.lifetime += 1

        # Varningsfas
        if self.lifetime < self.warning_duration:
            self.warning = True

        # Svepningsfas
        elif self.lifetime < self.warning_duration + self.sweep_duration:
            self.warning = False
            self.rect.x += self.speed

            # Inaktivera om utanför skärmen
            if self.direction > 0 and self.rect.x > 1920:
                self.active = False
            elif self.direction < 0 and self.rect.x < -self.rect.width:
                self.active = False
        else:
            self.active = False

    def draw(self, screen):
        """Rita snabb svepning med UFO"""
        if not self.active:
            return

        if self.warning:
            # Warning: Pulsing faded UFO on screen edge
            pulse_scale = 1.0 + 0.2 * math.sin(self.lifetime * 0.3)
            pulse_width = int(60 * pulse_scale)
            pulse_height = int(40 * pulse_scale)
            pulsed_ufo = pygame.transform.scale(self.ufo_image_original, (pulse_width, pulse_height))

            # Make it faded (50% opacity)
            pulsed_ufo.set_alpha(128)

            # Position on screen edge
            if self.direction > 0:
                ufo_x = self.warning_x
                ufo_y = self.rect.y + (self.rect.height - pulse_height) // 2
            else:
                ufo_x = self.warning_x + 80 - pulse_width
                ufo_y = self.rect.y + (self.rect.height - pulse_height) // 2

            screen.blit(pulsed_ufo, (ufo_x, ufo_y))
        else:
            # Attack: Full opacity UFO sweeping across
            screen.blit(self.ufo_image_sweep, self.rect)


class MultiSlam(Hitbox):
    """
    Multi-Slam - 3 tentaklar faller i sekvens vid olika X-positioner
    Wrapper för 3 TentacleSlam-objekt med delay
    """
    def __init__(self, target_positions, screen_shake_callback=None):
        """
        target_positions: Lista med 3 X-koordinater för tentaklarna
        """
        # Denna klass är en container, använder inte Hitbox direkt
        super().__init__(0, 0, 0, 0, damage=0)
        self.tentacles = []
        self.delays = [0, 30, 60]  # Delay mellan varje tentakel (0.5 sek mellan)

        for i, x_pos in enumerate(target_positions):
            tentacle = TentacleSlam(x_pos, 980, screen_shake_callback)
            self.tentacles.append({
                'tentacle': tentacle,
                'delay': self.delays[i],
                'started': False
            })

    def update(self):
        """Uppdatera alla tentaklar"""
        self.lifetime += 1

        # Starta tentaklar baserat på delay
        for t_data in self.tentacles:
            if not t_data['started'] and self.lifetime >= t_data['delay']:
                t_data['started'] = True

            if t_data['started']:
                t_data['tentacle'].update()

        # Inaktivera om alla tentaklar är klara
        if all(not t['tentacle'].active for t in self.tentacles):
            self.active = False

    def check_collision(self, player_rect):
        """Kolla kollision med någon av tentaklarna"""
        for t_data in self.tentacles:
            if t_data['started'] and t_data['tentacle'].check_collision(player_rect):
                return True
        return False

    def draw(self, screen):
        """Rita alla tentaklar"""
        for t_data in self.tentacles:
            if t_data['started']:
                t_data['tentacle'].draw(screen)


class BeamSweep(Hitbox):
    """
    Beam Sweep - ögonstråle som sveper från vänster till höger
    Warning: 120 frames (2 sekunder) - tunn linje följer player
    Sweep: 90 frames (1.5 sekunder) - tjock stråle sveper horisontellt
    """
    def __init__(self, boss_x, boss_y):
        super().__init__(boss_x, boss_y, 20, 1080 - boss_y, damage=0, color=(0, 255, 255))  # Reducerad damage till 0
        self.warning_duration = 120
        self.sweep_duration = 90
        self.warning = True
        self.boss_x = boss_x
        self.boss_y = boss_y
        self.sweep_start_x = 100
        self.sweep_end_x = 1820
        self.current_x = self.sweep_start_x
        self.warning_width = 5
        self.attack_width = 30

    def update(self):
        """Uppdatera beam sweep"""
        self.lifetime += 1

        # Varningsfas
        if self.lifetime < self.warning_duration:
            self.warning = True

        # Svepningsfas
        elif self.lifetime < self.warning_duration + self.sweep_duration:
            self.warning = False

            # Rör strålen från vänster till höger
            progress = (self.lifetime - self.warning_duration) / self.sweep_duration
            self.current_x = self.sweep_start_x + (self.sweep_end_x - self.sweep_start_x) * progress
            self.rect.x = self.current_x
        else:
            self.active = False

    def draw(self, screen):
        """Rita beam sweep"""
        if not self.active:
            return

        if self.warning:
            # Rita tunn varnings-linje vid start-position
            # TODO: Replace with beam sweep warning sprite (thin targeting line)
            pygame.draw.line(
                screen,
                (255, 255, 0),
                (self.sweep_start_x, self.boss_y),
                (self.sweep_start_x, 1080),
                self.warning_width
            )
        else:
            # Rita tjock svepande stråle
            # TODO: Replace with beam sweep attack sprite (thick sweeping laser)
            beam_rect = pygame.Rect(
                self.current_x - self.attack_width // 2,
                self.boss_y,
                self.attack_width,
                1080 - self.boss_y
            )
            pygame.draw.rect(screen, self.color, beam_rect)

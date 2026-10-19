import pygame
import random
import math
from projectile import (
    TentacleSlam, EyeBeam, ProjectileShot, GravityPull,
    FastSweep, MultiSlam, BeamSweep
)


class BossOctosaucer(pygame.sprite.Sprite):
    """UFO-bläckfisk boss med tre faser och attack-mönster"""

    # Boss states
    STATE_IDLE = "idle"              # Väntar innan attack
    STATE_ATTACKING = "attacking"     # Utför attack
    STATE_COOLDOWN = "cooldown"       # Väntar mellan attacker
    STATE_TRANSITION = "transition"   # Fas-övergång
    STATE_DEATH = "death"             # Dödsanimation

    # Attack phases
    PHASE_1 = 1  # HP 300-200
    PHASE_2 = 2  # HP 200-100
    PHASE_3 = 3  # HP 100-0

    # Tuning constants
    BOSS_DAMAGE_PER_JUMP = 10        # Skada per hopp på boss
    BOSS_BOUNCE_THRESHOLD = 50       # Pixels över boss.top för lyckat hopp (ökad för lättare träff)
    PLAYER_BOUNCE_VELOCITY = -15     # Studshastighet efter lyckat hopp

    def __init__(self, x, y, image_path):
        """
        Initialisera boss.

        Args:
            x: Start X-position
            y: Start Y-position (base, bobbing appliceras ovanpå)
            image_path: Sökväg till boss sprite
        """
        super().__init__()

        # Ladda boss-sprite
        try:
            self.base_image = pygame.image.load(image_path).convert_alpha()
            self.base_image = pygame.transform.scale(self.base_image, (300, 300))
        except:
            # Fallback om bilden inte finns
            self.base_image = pygame.Surface((300, 300))
            self.base_image.fill((128, 0, 128))

        self.image = self.base_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Boss stats
        self.max_hp = 300
        self.hp = 300
        self.phase = self.PHASE_1

        # Movement (horisontell rörelse + bobbing)
        self.base_x = x
        self.base_y = y
        self.target_x = x
        self.move_speed = 4  # Ökad från 2 till 4 för snabbare rörelse
        self.bob_offset = 0
        self.bob_speed = 0.08  # Ökad från 0.05 för snabbare bobbing
        self.bob_amplitude = 25  # Ökad från 20 för mer rörelse

        # State machine
        self.state = self.STATE_IDLE
        self.state_timer = 180  # Startar med 3 sekunders delay (spawn protection)

        # Attack system
        self.current_attack = None
        self.active_hitboxes = []
        self.active_gravity_pulls = []  # Separat lista för gravity pulls

        # Visual effects
        self.flash_timer = 0          # För vit blinkning vid skada
        self.tint_color = None        # Fas-färgning (cyan→magenta→röd)

        # Death animation
        self.death_timer = 120        # 2 sekunder flash
        self.death_flash = False

        # Invincibility tracking (triggers every 50 HP damage)
        self.last_invincible_hp = 300  # Track last HP threshold for invincibility

    def take_damage(self, amount):
        """
        Hantera skada, invincibility triggers, och fas-övergångar.
        Boss går invincible i 5 sekunder (300 frames) var 50:e HP.

        Args:
            amount: Mängd skada att applicera
        """
        old_hp = self.hp
        self.hp = max(0, self.hp - amount)
        self.flash_timer = 10  # Flash white for 10 frames

        # Kolla om boss är död
        if self.hp <= 0:
            self.start_death()
            return

        # Kolla om vi korsade en 50 HP threshold (250, 200, 150, 100, 50)
        # Beräkna vilket 50 HP-intervall vi är i
        current_threshold = (self.hp // 50) * 50
        last_threshold = (self.last_invincible_hp // 50) * 50

        if current_threshold < last_threshold:
            # Vi korsade en 50 HP threshold - trigga invincibility
            self.last_invincible_hp = self.hp

            # Kolla om detta också är en fas-övergång (200 eller 100 HP)
            if old_hp > 200 and self.hp <= 200:
                self.transition_to_phase(self.PHASE_2)
            elif old_hp > 100 and self.hp <= 100:
                self.transition_to_phase(self.PHASE_3)
            else:
                # Vanlig invincibility (ingen fas-ändring)
                self.enter_invincibility()

    def enter_invincibility(self):
        """
        Gå in i invincibility-läge utan att ändra fas.
        Används var 50:e HP (250, 150, 50).
        """
        self.state = self.STATE_TRANSITION
        self.state_timer = 300  # 5 sekunder invincibility (60 FPS * 5)

        # Rensa alla aktiva attacker
        self.active_hitboxes = []
        self.active_gravity_pulls = []
        # VIKTIGT: Ändra INTE fas eller tint_color här!

    def transition_to_phase(self, new_phase):
        """
        Fas-övergång med paus och färgändring.
        Samma invincibility-tid som vanlig invincibility (5 sekunder).

        Args:
            new_phase: Ny fas att övergå till (PHASE_2 eller PHASE_3)
        """
        self.state = self.STATE_TRANSITION
        self.phase = new_phase
        self.state_timer = 300  # 5 sekunder invincibility (samma som enter_invincibility)

        # Rensa alla aktiva attacker vid fas-övergång
        self.active_hitboxes = []
        self.active_gravity_pulls = []

        # Ändra ögonfärg via tint (permanent förändring för denna fas)
        if new_phase == self.PHASE_2:
            self.tint_color = (255, 0, 255)  # Magenta
        elif new_phase == self.PHASE_3:
            self.tint_color = (255, 0, 0)    # Röd

    def start_death(self):
        """Starta dödsanimation"""
        self.state = self.STATE_DEATH
        self.death_timer = 120  # 2 sekunder
        # Rensa alla aktiva attacker
        self.active_hitboxes = []
        self.active_gravity_pulls = []

    def pick_random_attack(self):
        """
        Välj slumpmässig attack baserat på fas med viktning.
        fast_sweep och gravity_pull används från start!

        Returns:
            String med attack-namn
        """
        # ALL ATTACKS AVAILABLE FROM START - fast_sweep very common!
        attacks = ["tentacle_slam", "eye_beam", "projectile_shot", "gravity_pull", "fast_sweep"]
        weights = [20, 15, 15, 15, 35]  # fast_sweep 35%, others lower

        # Use weighted random selection
        selected_attack = random.choices(attacks, weights=weights, k=1)[0]
        return selected_attack

    def get_attack_cooldown(self):
        """
        Beräkna attack cooldown baserat på nuvarande HP.
        Lägre HP = kortare cooldown = fler attacker.

        Returns:
            int: Cooldown i frames
        """
        # HP percentage (1.0 = full HP, 0.0 = no HP)
        hp_percent = self.hp / self.max_hp

        # Linear interpolation: 120 frames at full HP, 30 frames at 0 HP
        max_cooldown = 120  # 2.0 seconds
        min_cooldown = 30   # 0.5 seconds

        cooldown = max_cooldown - (max_cooldown - min_cooldown) * (1 - hp_percent)

        return int(cooldown)

    def start_attack(self, attack_name, player, screen_shake_callback):
        """
        Initiera specifik attack.

        Args:
            attack_name: Namn på attack att starta
            player: Spelarobjekt (för positioning)
            screen_shake_callback: Callback för screen shake
        """
        if attack_name == "tentacle_slam":
            # Sikta på spelarens position
            target_x = player.rect.centerx - 100
            slam = TentacleSlam(target_x, 980, screen_shake_callback)
            self.active_hitboxes.append(slam)

        elif attack_name == "eye_beam":
            # Vertikal stråle från boss position
            beam_x = self.rect.centerx - 50
            beam = EyeBeam(beam_x, self.rect.bottom, 100, 1080 - self.rect.bottom)
            self.active_hitboxes.append(beam)

        elif attack_name == "projectile_shot":
            # 3 projektiler i spread pattern
            center_x = self.rect.centerx
            for offset in [-100, 0, 100]:
                projectile = ProjectileShot(
                    center_x + offset,
                    self.rect.bottom,
                    radius=15,
                    vel_y=5
                )
                self.active_hitboxes.append(projectile)

        elif attack_name == "gravity_pull":
            # Gravitationsdragning i mitten av skärmen
            pull = GravityPull(960, 540, pull_radius=300, pull_strength=0.5)
            self.active_gravity_pulls.append(pull)

        elif attack_name == "fast_sweep":
            # Svepning från vänster eller höger (slumpmässig)
            direction = random.choice([1, -1])
            sweep = FastSweep(y=980, direction=direction)
            self.active_hitboxes.append(sweep)

        elif attack_name == "multi_slam":
            # 3 tentaklar vid olika positioner
            positions = [
                player.rect.centerx - 200,
                player.rect.centerx,
                player.rect.centerx + 200
            ]
            multi = MultiSlam(positions, screen_shake_callback)
            self.active_hitboxes.append(multi)

        elif attack_name == "beam_sweep":
            # Svepande ögonstråle
            beam_sweep = BeamSweep(self.rect.centerx, self.rect.bottom)
            self.active_hitboxes.append(beam_sweep)

    def update(self, player, screen_shake_callback):
        """
        Uppdatera boss AI och rörelse.

        Args:
            player: Spelarobjekt
            screen_shake_callback: Callback för screen shake

        Returns:
            Dictionary med event-data (player_damage, etc.) eller None
        """
        result = {}

        # Uppdatera state timer
        if self.state_timer > 0:
            self.state_timer -= 1

        # === MOVEMENT ===
        # Horisontell rörelse mot target
        if self.rect.x < self.target_x:
            self.rect.x = min(self.rect.x + self.move_speed, self.target_x)
        elif self.rect.x > self.target_x:
            self.rect.x = max(self.rect.x - self.move_speed, self.target_x)

        # Bobbing-rörelse (sinus-våg)
        self.bob_offset += self.bob_speed
        self.rect.y = int(self.base_y + self.bob_amplitude * math.sin(self.bob_offset))

        # Slumpmässigt byt target X ibland
        if random.randint(0, 300) == 0:
            self.target_x = random.randint(400, 1520)

        # === STATE MACHINE ===
        if self.state == self.STATE_IDLE:
            if self.state_timer == 0:
                # Välj attack
                self.current_attack = self.pick_random_attack()
                self.state = self.STATE_ATTACKING
                self.start_attack(self.current_attack, player, screen_shake_callback)

        elif self.state == self.STATE_ATTACKING:
            # Uppdatera aktiva hitboxes
            for hitbox in self.active_hitboxes[:]:
                hitbox.update()

                # Kolla kollision med spelaren
                if hitbox.check_collision(player.rect):
                    result['player_damage'] = hitbox.damage

                # Ta bort inaktiva hitboxes
                if not hitbox.active:
                    self.active_hitboxes.remove(hitbox)

            # Uppdatera gravity pulls (separat logik)
            for pull in self.active_gravity_pulls[:]:
                pull.update()

                # Applicera dragning på spelaren
                if pull.active and not pull.warning:
                    pull_force = pull.apply_pull(player)
                    if pull_force != (0, 0):
                        player.rect.x += int(pull_force[0])
                        player.rect.y += int(pull_force[1])

                # Kolla om spelaren når centrum (damage)
                if pull.check_collision(player.rect):
                    result['player_damage'] = pull.damage

                # Ta bort inaktiva pulls
                if not pull.active:
                    self.active_gravity_pulls.remove(pull)

            # Kolla om attack är klar
            if len(self.active_hitboxes) == 0 and len(self.active_gravity_pulls) == 0:
                self.state = self.STATE_COOLDOWN
                self.state_timer = self.get_attack_cooldown()

        elif self.state == self.STATE_COOLDOWN:
            if self.state_timer == 0:
                self.state = self.STATE_IDLE

        elif self.state == self.STATE_TRANSITION:
            # Vänta tills timer är klar
            if self.state_timer == 0:
                self.state = self.STATE_IDLE
                self.state_timer = 60  # 1 sekund innan nästa attack

        elif self.state == self.STATE_DEATH:
            # Dödsanimation
            self.death_timer -= 1
            self.death_flash = (self.death_timer // 10) % 2 == 0  # Flash varje 10 frames

            if self.death_timer == 0:
                result['boss_defeated'] = True

        # Uppdatera visuella effekter
        if self.flash_timer > 0:
            self.flash_timer -= 1

        # Uppdatera image för rendering
        display_image = self.get_display_image()
        if display_image:
            self.image = display_image

        return result if result else None

    def get_display_image(self):
        """
        Hämta boss-bilden med alla visuella effekter applicerade.
        Används för rendering i main.py med zoom.

        Returns:
            pygame.Surface: Boss-bild med effekter
        """
        # Death animation - försvinn
        if self.state == self.STATE_DEATH and self.death_timer == 0:
            return None  # Ingen bild om död

        # Basimage
        display_image = self.base_image.copy()

        # Applicera tint (fas-färg)
        if self.tint_color and self.state != self.STATE_DEATH:
            # Skapa en overlay med tint-färg
            tint_surface = pygame.Surface(display_image.get_size(), pygame.SRCALPHA)
            tint_surface.fill((*self.tint_color, 100))  # Semi-transparent
            display_image.blit(tint_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # TRANSITION state - visa tydlig invincibility-effekt
        if self.state == self.STATE_TRANSITION:
            # Pulserar vit overlay för att visa invincibility
            pulse_alpha = int(100 + 100 * abs(math.sin(self.state_timer * 0.1)))
            invincible_surface = pygame.Surface(display_image.get_size(), pygame.SRCALPHA)
            invincible_surface.fill((255, 255, 255, pulse_alpha))
            display_image.blit(invincible_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Flash vit vid skada (inte under transition eller death)
        elif self.flash_timer > 0:
            flash_surface = pygame.Surface(display_image.get_size(), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, 200))
            display_image.blit(flash_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # Death flash
        if self.state == self.STATE_DEATH and self.death_flash:
            flash_surface = pygame.Surface(display_image.get_size(), pygame.SRCALPHA)
            flash_surface.fill((255, 255, 255, 200))
            display_image.blit(flash_surface, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        return display_image

    def check_player_jump_damage(self, player):
        """
        Kolla om spelaren hoppar på boss för att göra skada.

        Args:
            player: Spelarobjekt

        Returns:
            Dictionary med 'boss_damage' och 'player_bounce' om lyckat hopp,
            'player_damage' om kollision från sida/under, eller None
        """
        # Ingen kollision om boss är död eller i transition
        if self.state == self.STATE_DEATH or self.state == self.STATE_TRANSITION:
            return None

        # Kolla kollision
        if not player.rect.colliderect(self.rect):
            return None

        # Kolla om spelaren hoppar på boss från ovan
        if (player.vel_y > 0 and
            player.rect.bottom <= self.rect.top + self.BOSS_BOUNCE_THRESHOLD):
            # Framgångsrikt hopp - skada boss!
            return {
                'boss_damage': self.BOSS_DAMAGE_PER_JUMP,
                'player_bounce': self.PLAYER_BOUNCE_VELOCITY
            }
        else:
            # Kollision från sida/underifrån - skada spelare
            return {
                'player_damage': 0
            }

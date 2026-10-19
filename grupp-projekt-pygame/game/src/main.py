import pygame
import os
import sys
import random
import math
from player import Player
from obstacle import Obstacle
from collectible import Collectible
from powerup import PowerUp
from menu import MainMenu, PauseMenu, GameOverMenu, VictoryMenu, LevelSelectMenu
from background import BackgroundManager
from enemy_player import EnemyPlayer
from flying_enemy import FlyingEnemy
from menu import SettingsMenu
from particles import ParticleManager
from menu import MainMenu, PauseMenu, GameOverMenu, VictoryMenu, LevelSelectMenu, SettingsMenu, ScoresMenu
from scores import add_score


# Dölj pygame welcome message och AVX2 warning
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

# Stäng av ljudsystemet för att undvika ALSA errors i WSL
# os.environ['SDL_AUDIODRIVER'] = 'dummy'  # DISABLED - This prevents all audio from playing

# talar om systemet att vi startar pygame
pygame.init()

# Aktivera key repeat för dubbelhopp
# (delay 200ms, interval 50ms) - gör att SPACE kan tryckas snabbare.
pygame.key.set_repeat(200, 50)

# Initiera mixer för ljud med bättre inställningar för WAV/MP3
# frequency=44100, size=-16 (16-bit signed), channels=2 (stereo), buffer=4096
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

# Hitta sökvägen till sounds-mappen
base_dir = os.path.dirname(__file__)
sounds_dir = os.path.join(base_dir, "..", "assets", "sounds")

# Musikfiler för olika levels
MENU_MUSIC = os.path.join(sounds_dir, "menu-music.wav")
LEVEL1_MUSIC = os.path.join(sounds_dir, "menu-music.wav")  # Level 1 uses menu music
LEVEL2_MUSIC = os.path.join(sounds_dir, "music-level-2.wav")
LEVEL3_MUSIC = os.path.join(sounds_dir, "boss-music.wav")

# Ladda ljudfiler för när spelaren samlar en svamp eller mynt
coin_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "coin.wav"))
special_coin_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "coin2.wav"))
special_coin_sound.set_volume(0.5)

# Ladda hit sound
hit_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "hit.wav"))
hit_sound.set_volume(0.6)

# Ladda boss death sound
boss_death_sound = pygame.mixer.Sound(os.path.join(sounds_dir, "boss-death.wav"))
boss_death_sound.set_volume(0.7)

# ============================================================================
# GLOBAL VOLUME STATE
# ============================================================================
class VolumeSettings:
    """Global volume settings for music and sound effects."""
    def __init__(self):
        self.music_volume = 0.5  # 0.0 to 1.0
        self.sfx_volume = 0.5    # 0.0 to 1.0

    def set_music_volume(self, volume):
        """Update music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)

    def set_sfx_volume(self, volume):
        """Update sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        coin_sound.set_volume(self.sfx_volume)
        hit_sound.set_volume(self.sfx_volume * 0.6)
        boss_death_sound.set_volume(self.sfx_volume * 0.7)

# Create global volume settings instance
volume_settings = VolumeSettings()

# Set initial volumes
coin_sound.set_volume(volume_settings.sfx_volume)
hit_sound.set_volume(volume_settings.sfx_volume * 0.6)
boss_death_sound.set_volume(volume_settings.sfx_volume * 0.7)

def switch_music(music_path):
    """
    Switch to a different music track.
    Stops current music and starts the new track.
    """
    if os.path.exists(music_path):
        pygame.mixer.music.stop()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.play(-1)   # loopa för evigt
        pygame.mixer.music.set_volume(volume_settings.music_volume)

# Starta menu music
switch_music(MENU_MUSIC)

# ---------------------------------------------------------------------------
# Konfiguration fiende – när får den vara aktiv?
# Screen 0,1,2 = bana 1, där ska fienden INTE synas.
# Vi aktiverar den först på framtida screens (ex. nästa bana).
# ---------------------------------------------------------------------------
ENEMY_ACTIVE_FROM_SCREEN = 3

"""här skapas spelfönstret, variablerna väljer man själv
inbyggd funktion i pygame är display mode och caption
(det som står högst upp på rutan är caption) sedan kallar vi på variablerna
när vi lägger in det på displayen
height representerar är y axeln, width representerar x axeln i det här fallet storleken på spelfönstret """
WIDTH = 1920
HEIGHT = 1080
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minil Tech 2D Spel")

# HUD resources
tilesets_dir = os.path.join(base_dir, "..", "assets", "tilesets")
sprites_dir = os.path.join(base_dir, "..", "assets", "sprites")

hud_mushroom_icon = pygame.image.load(
    os.path.join(tilesets_dir, "mashroom.png")
).convert_alpha()
hud_mushroom_icon = pygame.transform.scale(hud_mushroom_icon, (40, 40))

# Load heart icon for HUD (single asset, no fallback magic)
hud_heart_full = pygame.image.load(
    os.path.join(sprites_dir, "emptyheart.png")
    ).convert_alpha()
hud_heart_full = pygame.transform.scale(hud_heart_full, (32, 32))

# Create empty heart by dimming full heart
hud_heart_empty = hud_heart_full.copy()
hud_heart_empty.fill((255, 255, 255, 90), special_flags=pygame.BLEND_RGBA_MULT)

clock = pygame.time.Clock()
player = Player(100, 850, max_jumps=1)  # Start near bottom - Level 1 (single jump)

# Skapa enemies - två per screen (en längst ner, en högre upp)
image_dir = os.path.join(base_dir, "..", "assets", "sprites", "enemies")
enemy_bottom = EnemyPlayer(320, 690, image_dir)  # Bottom enemy - lower platform
enemy_top = EnemyPlayer(850, 350, image_dir)     # Top enemy - higher up, not too obstructive
# Fienden läggs till/aktiveras dynamiskt beroende på vilken screen vi är på
enemy_group = pygame.sprite.Group()
enemy_group.add(enemy_bottom)
enemy_group.add(enemy_top)

# Skapa background manager för level1
bg_manager = BackgroundManager(WIDTH, HEIGHT, "level1")

particle_manager = ParticleManager(WIDTH, HEIGHT, max_particles=200)

# Power-Ups
level1_powerups = []  # No powerups in Level 1

# Level 2 Power-Up - Fedora (on peak platform in Screen 3 - Level 2 Screen 1)
# Platform 6 in screen3: (850, 400, 110, 50) - peak platform
fedora_powerup = PowerUp(870, 370, width=50, height=40)  # On platform 6, Screen 3 (Level 2 Screen 1)
level2_powerups = [fedora_powerup]

# Level 3 Power-Up - Fedora före boss fight (Screen 8, platform 4)
# Platform 4 i screen8: Obstacle(890, 680, 120, 50)
fedora_level3 = PowerUp(910, 650, width=50, height=40)  # På platform 4, Screen 8
level3_powerups = [fedora_level3]

# Level 2 Flying Enemies - DISABLED (too buggy)
# Flying enemies (octopus) have been disabled due to buggy movement
level2_flying_enemies = {}
# level2_flying_enemies = {
#     3: [  # Screen 3: 2 enemies
#         FlyingEnemy(800, 300),
#         FlyingEnemy(1500, 400)
#     ],
#     4: [  # Screen 4: 3 enemies (more challenging)
#         FlyingEnemy(600, 250),
#         FlyingEnemy(1200, 350),
#         FlyingEnemy(1800, 300)
#     ],
#     5: [  # Screen 5: 4 enemies (high threat)
#         FlyingEnemy(500, 300),
#         FlyingEnemy(1000, 400),
#         FlyingEnemy(1500, 250),
#         FlyingEnemy(2000, 350)
#     ],
#     6: [  # Screen 6: 4 enemies (continued challenge)
#         FlyingEnemy(700, 400),
#         FlyingEnemy(1100, 300),
#         FlyingEnemy(1500, 450),
#         FlyingEnemy(1800, 350)
#     ],
#     7: [  # Screen 7: 5 enemies (MAXIMUM THREAT!)
#         FlyingEnemy(400, 350),
#         FlyingEnemy(800, 300),
#         FlyingEnemy(1200, 400),
#         FlyingEnemy(1600, 300),
#         FlyingEnemy(1900, 450)
#     ]
# }

# Level 3 Boss Fight - initialiseras när Level 3 startas
boss_octosaucer = None
boss_camera = None
boss_victory_delay = 0  # Delay before transitioning to victory screen after boss death
screen_shake_timer = 0
screen_shake_intensity = 8

# pygame känner igen färger via tuple väljer färg via RGB
# sedan kallar vi på "variabeln" genom att använda den inbyggda funktionen i pygame screen.fill
BACKGROUND_COLOR = (0, 255, 0)

# ============================================================================
# LEVEL 1 - PYRAMID CLIMBING CHALLENGE (1920x1080)
# ============================================================================
# NO GROUND FLOOR - Background image is the ground!
# Players climb progressively higher platforms like climbing a pyramid
# Uses MAXIMUM vertical space - platforms go from bottom (900) to top (100)
# Collectibles placed at peak positions for maximum challenge
#
# Design philosophy: CLIMB HIGH, REACH THE SKY!

# SCREEN 0: Vertical Platforming with Backwards Movement!
screen0_obstacles = [
    # Start low, climb high, drop down, repeat - with BIG GAPS for falling
    Obstacle(100, 900, 140, 50),           # 1. Start platform (low)
    # GAP - can fall through!
    Obstacle(320, 730, 130, 50),           # 2. Jump up high!
    # GAP
    Obstacle(530, 860, 140, 50),           # 3. Drop back down
    # GAP
    Obstacle(760, 660, 130, 50),           # 4. Climb up again
    # GAP - BACKWARDS SECTION!
    Obstacle(640, 520, 120, 50),           # 5. Jump BACK (left) to go higher!
    # GAP
    Obstacle(850, 380, 130, 50),           # 6. Now jump forward again (very high)
    # GAP
    Obstacle(1070, 580, 140, 50),          # 7. Drop down mid
    # GAP
    Obstacle(1300, 700, 130, 50),          # 8. Lower platform
    # GAP - Another backwards!
    Obstacle(1180, 570, 120, 50),          # 9. Jump BACK for better position
    # GAP
    Obstacle(1420, 460, 130, 50),          # 10. Jump forward high
    # GAP
    Obstacle(1650, 680, 130, 50),          # 11. Drop to mid
    # GAP
    Obstacle(1870, 850, 120, 50),          # 12. Exit platform (syncs with next screen start)
]

# SCREEN 1: More Challenging with Multiple Backwards Jumps!
screen1_obstacles = [
    # Even more vertical variation and bigger gaps
    Obstacle(80, 860, 130, 50),            # 1. Start mid-low
    # GAP
    Obstacle(280, 630, 120, 50),           # 2. Jump up high
    # GAP - BACKWARDS!
    Obstacle(160, 480, 110, 50),           # 3. Jump BACK to go higher
    # GAP
    Obstacle(370, 340, 120, 50),           # 4. Jump forward - very high!
    # GAP
    Obstacle(590, 570, 130, 50),           # 5. Drop down mid
    # GAP
    Obstacle(820, 730, 120, 50),           # 6. Lower platform
    # GAP - BACKWARDS AGAIN!
    Obstacle(700, 590, 110, 50),           # 7. Jump BACK for positioning
    # GAP
    Obstacle(920, 440, 120, 50),           # 8. Forward jump - high
    # GAP
    Obstacle(1140, 630, 130, 50),          # 9. Mid platform
    # GAP - TRICKY BACKWARDS!
    Obstacle(1010, 510, 110, 50),          # 10. Jump BACK to small platform
    # GAP
    Obstacle(1240, 360, 120, 50),          # 11. Forward - very high
    # GAP
    Obstacle(1460, 570, 130, 50),          # 12. Drop mid
    # GAP
    Obstacle(1680, 460, 120, 50),          # 13. Higher platform
    # GAP
    Obstacle(1880, 800, 110, 50),          # 14. Exit platform (syncs with next screen start)
]

# SCREEN 2: Advanced Gauntlet - Master the Backwards Jump!
screen2_obstacles = [
    # Extreme vertical challenges with complex backwards patterns
    Obstacle(70, 810, 120, 50),            # 1. Start mid
    # GAP
    Obstacle(260, 580, 120, 50),           # 2. Jump up
    # GAP - BACKWARDS START!
    Obstacle(140, 440, 110, 50),           # 3. Jump BACK to go higher
    # GAP
    Obstacle(350, 300, 110, 50),           # 4. Forward - very high!
    # GAP
    Obstacle(550, 520, 120, 50),           # 5. Drop down
    # GAP
    Obstacle(770, 730, 110, 50),           # 6. Lower platform
    # GAP - BACKWARDS CHAIN!
    Obstacle(650, 620, 105, 50),           # 7. Jump BACK
    # GAP
    Obstacle(420, 450, 100, 50),           # 8. BACK AGAIN to small platform
    # GAP
    Obstacle(740, 280, 110, 50),           # 9. Forward - PEAK HEIGHT!
    # GAP
    Obstacle(940, 470, 120, 50),           # 10. Drop down (shifted left to avoid overlap with platform 12)
    # GAP - TRICKY BACKWARDS!
    Obstacle(840, 590, 105, 50),           # 11. Jump BACK for positioning
    # GAP
    Obstacle(1070, 460, 110, 50),          # 12. Forward high
    # GAP
    Obstacle(1280, 630, 120, 50),          # 13. Mid platform
    # GAP
    Obstacle(1490, 440, 110, 50),          # 14. High platform
    # GAP - FINAL BACKWARDS!
    Obstacle(1370, 510, 105, 50),          # 15. Jump BACK one last time
    # GAP
    Obstacle(1600, 340, 110, 50),          # 16. Forward to peak
    # GAP
    Obstacle(1820, 950, 110, 50),          # 17. FINAL VICTORY PLATFORM! (VERY LOW - one-way!)
]

# ============================================================================
# LEVEL 2 - ADVANCED PYRAMID CHALLENGE (1920x1080)
# ============================================================================
# Increased difficulty: smaller platforms, bigger gaps, more backwards jumps
# Enemy active throughout (starts at screen 3)

# SCREEN 3: Level 2 Introduction - Moderate Challenge
screen3_obstacles = [
    # Progressive climb with tighter platforms and larger gaps
    Obstacle(100, 880, 115, 50, "cloud_c"),           # 1. Start platform
    Obstacle(300, 740, 110, 50, "cloud_c"),            # 2. Jump up high
    Obstacle(520, 850, 115, 50, "cloud_c"),           # 3. Drop down
    Obstacle(740, 680, 110, 50, "cloud_c"),            # 4. Climb high
    Obstacle(600, 530, 105, 50, "cloud_c"),            # 5. BACKWARDS - Jump BACK higher
    Obstacle(850, 400, 110, 50, "cloud_c"),            # 6. Forward to peak
    Obstacle(1040, 620, 115, 50, "cloud_c"),          # 7. Drop mid-level (shifted left to avoid overlap with platform 9)
    Obstacle(1280, 760, 110, 50, "cloud_c"),           # 8. Lower platform
    Obstacle(1150, 610, 105, 50, "cloud_c"),           # 9. BACKWARDS - Jump BACK for positioning
    Obstacle(1390, 470, 110, 50, "cloud_c"),           # 10. Forward to high platform
    Obstacle(1600, 680, 115, 50, "cloud_c"),          # 11. Drop to mid
    Obstacle(1470, 550, 105, 50, "cloud_c"),           # 12. BACKWARDS - Jump BACK
    Obstacle(1710, 390, 110, 50, "cloud_c"),           # 13. Forward peak
    Obstacle(1900, 810, 110, 50, "cloud_c"),           # 14. Exit platform
]

# SCREEN 4: Medium Challenge - Backwards Chains Begin
screen4_obstacles = [
    Obstacle(90, 850, 110, 50, "cloud_c"),             # 1. Start mid-low
    Obstacle(310, 710, 105, 50, "cloud_c"),            # 2. Jump up
    Obstacle(180, 570, 105, 50, "cloud_c"),            # 3. BACKWARDS - Jump BACK to go higher
    Obstacle(400, 430, 110, 50, "cloud_c"),            # 4. Forward - very high!
    Obstacle(620, 640, 115, 50, "cloud_c"),           # 5. Drop down mid
    Obstacle(850, 760, 110, 50, "cloud_c"),            # 6. Lower platform
    Obstacle(510, 620, 105, 50, "cloud_c"),            # 7. BACKWARDS - Jump BACK (moved left)
    Obstacle(540, 480, 105, 50, "cloud_c"),            # 8. BACKWARDS - BACK AGAIN (chain)
    Obstacle(770, 340, 110, 50, "cloud_c"),            # 9. Forward - PEAK
    Obstacle(990, 560, 115, 50, "cloud_c"),           # 10. Drop down
    Obstacle(700, 680, 105, 50, "cloud_c"),            # 11. BACKWARDS - Jump BACK (moved left to avoid overlap with platform 6)
    Obstacle(1100, 460, 110, 50, "cloud_c"),           # 12. Forward high
    Obstacle(1310, 650, 115, 50, "cloud_c"),          # 13. Mid platform
    Obstacle(1530, 420, 105, 50, "cloud_c"),           # 14. High platform
    Obstacle(1750, 680, 110, 50, "cloud_c"),           # 15. Drop mid
    Obstacle(1900, 840, 105, 50, "cloud_c"),           # 16. Exit platform
]

# SCREEN 5: Final Challenge - Master Difficulty
screen5_obstacles = [
    Obstacle(80, 820, 105, 50, "cloud_c"),             # 1. Start mid
    Obstacle(290, 660, 100, 50, "cloud_c"),            # 2. Jump up (small)
    Obstacle(160, 510, 100, 50, "cloud_c"),            # 3. BACKWARDS - Jump BACK higher
    Obstacle(390, 370, 105, 50, "cloud_c"),            # 4. Forward very high (shifted right to avoid overlap)
    Obstacle(590, 600, 110, 50, "cloud_c"),            # 5. Drop down (shifted left to avoid overlap)
    Obstacle(820, 740, 100, 50, "cloud_c"),            # 6. Lower platform (small)
    Obstacle(710, 630, 100, 50, "cloud_c"),            # 7. BACKWARDS - Jump BACK (shifted right to avoid overlap)
    Obstacle(510, 490, 100, 50, "cloud_c"),            # 8. BACKWARDS - BACK AGAIN
    Obstacle(330, 350, 100, 50, "cloud_c"),            # 9. BACKWARDS - BACK THIRD TIME (chain of 3!) (shifted left to avoid overlap)
    Obstacle(570, 280, 105, 50, "cloud_c"),            # 10. Forward - ABSOLUTE PEAK
    Obstacle(800, 470, 100, 50, "cloud_c"),            # 11. Drop down (small)
    Obstacle(650, 590, 100, 50, "cloud_c"),            # 12. BACKWARDS - Jump BACK (shifted left to avoid overlap)
    Obstacle(900, 450, 105, 50, "cloud_c"),            # 13. Forward high
    Obstacle(1120, 640, 110, 50, "cloud_c"),           # 14. Mid platform
    Obstacle(980, 530, 100, 50, "cloud_c"),            # 15. BACKWARDS - Jump BACK
    Obstacle(1220, 400, 105, 50, "cloud_c"),           # 16. Forward to peak
    Obstacle(1440, 630, 100, 50, "cloud_c"),           # 17. Drop mid (small)
    Obstacle(1660, 480, 105, 50, "cloud_c"),           # 18. High platform
    Obstacle(1820, 950, 105, 50, "cloud_c"),           # 19. Exit to next screen
]

# SCREEN 6: Continued Challenge (reuses background moln1.png)
screen6_obstacles = [
    Obstacle(90, 850, 110, 50, "cloud_c"),           # 1. Start mid-low
    Obstacle(310, 710, 105, 50, "cloud_c"),          # 2. Jump up
    Obstacle(180, 570, 105, 50, "cloud_c"),          # 3. BACKWARDS - Jump BACK to go higher
    Obstacle(400, 430, 110, 50, "cloud_c"),          # 4. Forward - very high!
    Obstacle(620, 640, 115, 50, "cloud_c"),         # 5. Drop down mid
    Obstacle(850, 760, 110, 50, "cloud_c"),          # 6. Lower platform
    Obstacle(510, 620, 105, 50, "cloud_c"),          # 7. BACKWARDS - Jump BACK (moved left)
    Obstacle(540, 480, 105, 50, "cloud_c"),          # 8. BACKWARDS - BACK AGAIN (chain)
    Obstacle(770, 340, 110, 50, "cloud_c"),          # 9. Forward - PEAK
    Obstacle(990, 560, 115, 50, "cloud_c"),         # 10. Drop down
    Obstacle(700, 680, 105, 50, "cloud_c"),          # 11. BACKWARDS - Jump BACK (moved left to avoid overlap with platform 6)
    Obstacle(1100, 460, 110, 50, "cloud_c"),         # 12. Forward high
    Obstacle(1310, 650, 115, 50, "cloud_c"),        # 13. Mid platform
    Obstacle(1530, 420, 105, 50, "cloud_c"),         # 14. High platform
    Obstacle(1750, 680, 110, 50, "cloud_c"),         # 15. Drop mid
    Obstacle(1900, 840, 105, 50, "cloud_c"),         # 16. Exit platform
]

# SCREEN 7: Final Victory Screen (reuses background moln3.png)
# FINAL VICTORY PLATFORM
screen7_obstacles = [
    Obstacle(80, 820, 105, 50, "cloud_c"),             # 1. Start mid
    Obstacle(290, 660, 100, 50, "cloud_c"),            # 2. Jump up (small)
    Obstacle(160, 510, 100, 50, "cloud_c"),            # 3. BACKWARDS - Jump BACK higher
    Obstacle(390, 370, 105, 50, "cloud_c"),            # 4. Forward very high (shifted right to avoid overlap)
    Obstacle(590, 600, 110, 50, "cloud_c"),            # 5. Drop down (shifted left to avoid overlap)
    Obstacle(820, 740, 100, 50, "cloud_c"),            # 6. Lower platform (small)
    Obstacle(710, 630, 100, 50, "cloud_c"),            # 7. BACKWARDS - Jump BACK (shifted right to avoid overlap)
    Obstacle(510, 490, 100, 50, "cloud_c"),            # 8. BACKWARDS - BACK AGAIN
    Obstacle(330, 350, 100, 50, "cloud_c"),            # 9. BACKWARDS - BACK THIRD TIME (chain of 3!) (shifted left to avoid overlap)
    Obstacle(570, 280, 105, 50, "cloud_c"),            # 10. Forward - ABSOLUTE PEAK
    Obstacle(800, 470, 100, 50, "cloud_c"),            # 11. Drop down (small)
    Obstacle(650, 590, 100, 50, "cloud_c"),            # 12. BACKWARDS - Jump BACK (shifted left to avoid overlap)
    Obstacle(900, 450, 105, 50, "cloud_c"),            # 13. Forward high
    Obstacle(1120, 640, 110, 50, "cloud_c"),           # 14. Mid platform
    Obstacle(980, 530, 100, 50, "cloud_c"),            # 15. BACKWARDS - Jump BACK
    Obstacle(1220, 400, 105, 50, "cloud_c"),           # 16. Forward to peak
    Obstacle(1440, 630, 100, 50, "cloud_c"),           # 17. Drop mid (small)
    Obstacle(1660, 480, 105, 50, "cloud_c"),           # 18. High platform
    Obstacle(1820, 950, 105, 50, "cloud_c"),           # 19. FINAL VICTORY PLATFORM!!!
]

# ============================================================================
# LEVEL 3 - BOSS FIGHT (1920x1080)
# ============================================================================
# Three screens: Approach (8), Boss Arena (9), Victory (10)

# SCREEN 8: The Approach - Simple platforming before boss
screen8_obstacles = [
    Obstacle(100, 900, 130, 50, "platform-level-3"),   # 1. Start platform
    Obstacle(350, 750, 120, 50, "platform-level-3"),   # 2. Jump up
    Obstacle(620, 820, 130, 50, "platform-level-3"),   # 3. Mid platform
    Obstacle(890, 680, 120, 50, "platform-level-3"),   # 4. Higher jump
    Obstacle(1160, 790, 130, 50, "platform-level-3"),  # 5. Drop down
    Obstacle(1450, 860, 140, 50, "platform-level-3"),  # 6. Final approach
    Obstacle(1750, 950, 150, 50, "platform-level-3"),  # 7. Exit platform (leads to boss)
]

# SCREEN 9: Boss Arena - MUCH WIDER platforms with BIG VERTICAL gaps
screen9_obstacles = [
    Obstacle(0, 1030, 1920, 70, "platform-level-3"),       # Floor (full width)
    # Vänster sida - SUPER WIDE platforms with BIG gaps (200px vertical spacing)
    Obstacle(5, 950, 250, 80, "platform-level-3"),        # Bottom left (VERY WIDE)
    Obstacle(140, 750, 250, 80, "platform-level-3"),        # Middle left (200px gap)
    Obstacle(5, 550, 250, 80, "platform-level-3"),        # Top left (200px gap)
    # Höger sida - SUPER WIDE platforms with BIG gaps (200px vertical spacing)
    Obstacle(1600, 950, 250, 80, "platform-level-3"),      # Bottom right (VERY WIDE)
    Obstacle(1400, 750, 250, 80, "platform-level-3"),      # Middle right (200px gap)
    Obstacle(1600, 550, 250, 80, "platform-level-3"),      # Top right (200px gap)
    # Center platforms near boss - WIDER
    Obstacle(600, 520, 250, 80, "platform-level-3"),       # Left of boss (WIDER)
    Obstacle(1070, 520, 250, 80, "platform-level-3"),      # Right of boss (WIDER)
]

# SCREEN 10: Victory Screen - Empty arena, boss is gone
screen10_obstacles = [
    Obstacle(0, 1030, 1920, 50, "platform-level-3"),       # Floor only
]

# All obstacles indexed by screen
all_screen_obstacles = [screen0_obstacles, screen1_obstacles, screen2_obstacles,
                        screen3_obstacles, screen4_obstacles, screen5_obstacles,
                        screen6_obstacles, screen7_obstacles,
                        screen8_obstacles, screen9_obstacles, screen10_obstacles]

# ============================================================================
# COLLECTIBLES - Mushrooms at pyramid peaks!
# ============================================================================

# SCREEN 0: Collectibles on platforms with backwards movement
screen0_collectibles = [
    Collectible(150, 870),                 # On start platform
    Collectible(370, 700),                 # On platform 2
    Collectible(580, 830),                 # On platform 3
    Collectible(810, 630),                 # On platform 4
    Collectible(690, 490),                 # On backwards platform 5!
    Collectible(900, 350),                 # On very high platform 6
    Collectible(1120, 550),                # On platform 7
    Collectible(1230, 540),                # On backwards platform 9!
    Collectible(1470, 430),                # On platform 10
    Collectible(1700, 650),                # On platform 11
    # Removed unreachable collectible at screen edge (1920, 820)
]

# SCREEN 1: More collectibles with backwards jumps
screen1_collectibles = [
    Collectible(130, 830),                 # On start platform
    Collectible(330, 600),                 # On platform 2
    Collectible(210, 450),                 # On backwards platform 3!
    Collectible(420, 310),                 # On very high platform 4
    Collectible(640, 540),                 # On platform 5
    Collectible(750, 560),                 # On backwards platform 7!
    Collectible(1060, 480),                # On backwards platform 10!
    Collectible(1290, 330),                # On very high platform 11
    Collectible(1510, 540),                # On platform 12
    Collectible(1730, 430),                # On platform 13
    # Removed unreachable collectible past screen edge (1925, 770)
]

# SCREEN 2: Advanced with complex backwards patterns
screen2_collectibles = [
    Collectible(120, 780),                 # On start platform
    Collectible(310, 550),                 # On platform 2
    Collectible(190, 410),                 # On backwards platform 3!
    Collectible(400, 270),                 # On very high platform 4
    Collectible(600, 490),                 # On platform 5
    Collectible(700, 590),                 # On backwards platform 7!
    Collectible(460, 420),                 # On backwards platform 8!
    Collectible(790, 250),                 # On PEAK platform 9!
    Collectible(990, 440),                 # On platform 10 (adjusted for platform shift)
    Collectible(890, 560),                 # On backwards platform 11!
    Collectible(1120, 430),                # On platform 12
    Collectible(1330, 600),                # On platform 13
    Collectible(1650, 310),                # On peak platform 16
    Collectible(1845, 920),                # On VICTORY platform! (left side for easy collection)
]

# SCREEN 3: Level 2 Introduction Collectibles
screen3_collectibles = [
    Collectible(150, 850),                 # On start platform
    Collectible(350, 710),                 # On platform 2
    Collectible(570, 820),                 # On platform 3
    Collectible(790, 650),                 # On platform 4
    Collectible(650, 500),                 # On backwards platform 5
    Collectible(925, 370),                 # On peak platform 6 (moved right for spacing from fedora)
    Collectible(1090, 590),                # On platform 7 (adjusted for platform shift)
    Collectible(1200, 580),                # On backwards platform 9
    Collectible(1440, 440),                # On platform 10
    Collectible(1650, 650),                # On platform 11
    Collectible(1520, 520),                # On backwards platform 12
    Collectible(1760, 360),                # On peak platform 13
]

# SCREEN 4: Medium Challenge Collectibles
screen4_collectibles = [
    Collectible(140, 820),                 # On start platform
    Collectible(360, 680),                 # On platform 2
    Collectible(230, 540),                 # On backwards platform 3
    Collectible(450, 400),                 # On high platform 4
    Collectible(670, 610),                 # On platform 5
    Collectible(900, 730),                 # On platform 6
    Collectible(560, 590),                 # On backwards platform 7 (adjusted for platform move)
    Collectible(590, 450),                 # On backwards platform 8 (chain)
    Collectible(820, 315),                 # On PEAK platform 9 (right side, fedora on left side)
    Collectible(1040, 530),                # On platform 10
    Collectible(750, 650),                 # On backwards platform 11 (adjusted for platform move)
    Collectible(1150, 430),                # On platform 12
    Collectible(1360, 620),                # On platform 13
    Collectible(1580, 390),                # On high platform 14
]

# SCREEN 5: Final Challenge Collectibles
screen5_collectibles = [
    Collectible(130, 790),                 # On start platform
    Collectible(340, 630),                 # On platform 2 (small)
    Collectible(210, 480),                 # On backwards platform 3
    Collectible(440, 340),                 # On high platform 4 (adjusted for platform shift)
    Collectible(640, 570),                 # On platform 5 (adjusted for platform shift)
    Collectible(870, 710),                 # On platform 6 (small)
    Collectible(760, 600),                 # On backwards platform 7 (adjusted for platform shift)
    Collectible(560, 460),                 # On backwards platform 8 (chain)
    Collectible(380, 320),                 # On backwards platform 9 (chain) (adjusted for platform shift)
    Collectible(620, 250),                 # On ABSOLUTE PEAK platform 10
    Collectible(850, 440),                 # On platform 11 (small)
    Collectible(680, 560),                 # On backwards platform 12 (adjusted for better spacing)
    Collectible(950, 420),                 # On platform 13
    Collectible(1170, 610),                # On platform 14
    Collectible(1030, 500),                # On backwards platform 15
    Collectible(1270, 370),                # On peak platform 16
    Collectible(1490, 600),                # On platform 17 (small)
    Collectible(1710, 450),                # On platform 18
    Collectible(1845, 920),                # On exit platform (moved left for easier collection, matching Level 1)
]

# SCREEN 6: Continued Challenge Collectibles (reuses background moln1.png)
screen6_collectibles = [
    Collectible(140, 820),                 # On start platform
    Collectible(360, 680),                 # On platform 2
    Collectible(230, 540),                 # On backwards platform 3
    Collectible(450, 400),                 # On high platform 4
    Collectible(670, 610),                 # On platform 5
    Collectible(900, 730),                 # On platform 6
    Collectible(560, 590),                 # On backwards platform 7 (adjusted for platform move)
    Collectible(590, 450),                 # On backwards platform 8 (chain)
    Collectible(820, 310),                 # On PEAK platform 9
    Collectible(1040, 530),                # On platform 10
    Collectible(750, 650),                 # On backwards platform 11 (adjusted for platform move)
    Collectible(1150, 430),                # On platform 12
    Collectible(1360, 620),                # On platform 13
    Collectible(1580, 390),                # On high platform 14
]

# SCREEN 7: Final Victory Collectibles (reuses background moln3.png)
screen7_collectibles = [
    Collectible(130, 790),                 # On start platform
    Collectible(340, 630),                 # On platform 2 (small)
    Collectible(210, 480),                 # On backwards platform 3
    Collectible(440, 340),                 # On high platform 4 (adjusted for platform shift)
    Collectible(640, 570),                 # On platform 5 (adjusted for platform shift)
    Collectible(870, 710),                 # On platform 6 (small)
    Collectible(760, 600),                 # On backwards platform 7 (adjusted for platform shift)
    Collectible(560, 460),                 # On backwards platform 8 (chain)
    Collectible(380, 320),                 # On backwards platform 9 (chain) (adjusted for platform shift)
    Collectible(620, 250),                 # On ABSOLUTE PEAK platform 10
    Collectible(850, 440),                 # On platform 11 (small)
    Collectible(680, 560),                 # On backwards platform 12 (adjusted for better spacing)
    Collectible(950, 420),                 # On platform 13
    Collectible(1170, 610),                # On platform 14
    Collectible(1030, 500),                # On backwards platform 15
    Collectible(1270, 370),                # On peak platform 16
    Collectible(1490, 600),                # On platform 17 (small)
    Collectible(1710, 450),                # On platform 18
    Collectible(1845, 920),                # On FINAL VICTORY PLATFORM!!! (moved left for easier collection, matching Level 1)
]

# SCREEN 8: Approach collectibles
screen8_collectibles = [
    Collectible(150, 870),   # On platform 1
    Collectible(400, 720),   # On platform 2
    Collectible(670, 790),   # On platform 3
    Collectible(940, 650),   # On platform 4
    Collectible(1210, 760),  # On platform 5
    Collectible(1500, 830),  # On platform 6
]

# SCREEN 9: Boss Arena - NO COLLECTIBLES (boss fight)
screen9_collectibles = []

# SCREEN 10: Victory Screen - NO COLLECTIBLES
screen10_collectibles = []

# All collectibles indexed by screen
all_screen_collectibles = [screen0_collectibles, screen1_collectibles, screen2_collectibles,
                           screen3_collectibles, screen4_collectibles, screen5_collectibles,
                           screen6_collectibles, screen7_collectibles,
                           screen8_collectibles, screen9_collectibles, screen10_collectibles]

def get_level_collectibles_count(level):
    """
    Get the total number of collectibles for a specific level.
    Level 1: screens 0-2 (36 collectibles)
    Level 2: screens 3-7 (78 collectibles)
    Level 3: screens 8-10 (6 collectibles - only on approach)
    """
    if level == 1:
        return sum(len(all_screen_collectibles[i]) for i in range(0, 3))
    elif level == 2:
        return sum(len(all_screen_collectibles[i]) for i in range(3, 8))
    else:  # Level 3
        return sum(len(all_screen_collectibles[i]) for i in range(8, 11))

# Track collection stats and lives
game_stats = {
    'total_collected': 0,
    'total_collectibles': get_level_collectibles_count(1),
    'lives': 3,
    'max_lives': 3,

    # scoring
    'level_score': 0,
    'total_score': 0,
    'level_start_ticks': pygame.time.get_ticks(),
    'level_time_seconds': 0
}
game_stats["run_saved"] = False  # Track if current run has been saved
# Level tracking
current_level = 1
LEVEL_1_FINAL_SCREEN = 2
LEVEL_2_FINAL_SCREEN = 7  # Updated: Level 2 now has 5 screens (3, 4, 5, 6, 7)
LEVEL_3_FINAL_SCREEN = 10  # Level 3: screens 8-10 (Approach, Boss Arena, Victory)

# Cooldown för enemy damage (förhindrar kontinuerlig skada)
enemy_damage_cooldown = 0
ENEMY_DAMAGE_COOLDOWN_TIME = 60  # 1 sekund vid 60 FPS

# Death zone - if player falls below this Y position, they die
DEATH_ZONE_Y = HEIGHT + 100  # 100 pixels below screen

# ============================================================================
# MENY-SYSTEM
# ============================================================================
# Spelet använder ett state-baserat meny-system med fyra tillstånd:
# - "main_menu": Huvudmeny visas, spelet har inte startat
# - "playing": Spelet körs aktivt
# - "paused": Spelet är pausat, pausmeny visas ovanpå fryst spel
# - "game_over": Spelaren har dött, game over-skärm visas

# Skapa huvudmeny med bakgrundsbild
# Bakgrundsbilden ligger i assets/menu/menybild-pepe.png
menu_background_path = os.path.join(base_dir, "..", "assets", "menu", "menybild-pepe.png")

main_menu = MainMenu(WIDTH, HEIGHT, menu_background_path)  # Huvudmeny med bakgrund
pause_menu = PauseMenu(WIDTH, HEIGHT)  # Pausmeny (ingen bakgrund, ritas över spelet)
settings_menu = SettingsMenu(WIDTH, HEIGHT, volume_settings)
game_over_menu = GameOverMenu(WIDTH, HEIGHT)  # Game over-skärm (ingen bakgrund, ritas över spelet)
victory_menu = VictoryMenu(WIDTH, HEIGHT)  # Victory screen (shown when completing all levels)
level_select_menu = LevelSelectMenu(WIDTH, HEIGHT)  # Level selection menu
scores_menu = ScoresMenu(WIDTH, HEIGHT, menu_background_path)

# Level unlocking system
level2_unlocked = True  # Tracks if Level 2 is unlocked

# Initialt speltillstånd: börja på huvudmenyn
game_state = "main_menu"

# Startposition för spelaren (används vid restart)
PLAYER_START_X = 100
PLAYER_START_Y = 850


def restart_current_level():
    """
    Restart the current level (keeps you in Level 1, 2, or 3).
    Called when player runs out of lives and clicks "restart" in game over menu.
    """
    global player, bg_manager, enemy_damage_cooldown, boss_octosaucer, boss_camera, boss_victory_delay

    # Determine level settings based on current_level
    if current_level == 1:
        level_name = "level1"
        start_screen = 0
        max_jumps = 1
        switch_music(LEVEL1_MUSIC)  # Switch to Level 1 music
    elif current_level == 2:
        level_name = "level2"
        start_screen = 3
        max_jumps = 2
        switch_music(LEVEL2_MUSIC)  # Switch to Level 2 music
    else:  # Level 3
        level_name = "level3"
        start_screen = 8  # Börja på approach screen
        max_jumps = 2
        switch_music(LEVEL3_MUSIC)  # Switch to Level 3 music
        # Reset boss och kamera för clean restart
        boss_octosaucer = None
        boss_camera = None
        boss_victory_delay = 0

    # Recreate player and background manager
    player = Player(PLAYER_START_X, PLAYER_START_Y, max_jumps=max_jumps)
    bg_manager = BackgroundManager(WIDTH, HEIGHT, level_name)
    bg_manager.current_index = start_screen

    # Reset collectibles for current level only
    if current_level == 1:
        # Reset screens 0-2 (Level 1)
        for i in range(0, 3):
            for collectible in all_screen_collectibles[i]:
                collectible.collected = False
    elif current_level == 2:
        # Reset screens 3-7 (Level 2)
        for i in range(3, 8):
            for collectible in all_screen_collectibles[i]:
                collectible.collected = False
        # Reset power-ups
        for powerup in level1_powerups:
            powerup.collected = False
        for powerup in level2_powerups:
            powerup.collected = False
    else:  # Level 3
        # Reset screens 8-10 (Level 3)
        for i in range(8, 11):
            for collectible in all_screen_collectibles[i]:
                collectible.collected = False
        # Reset power-ups
        for powerup in level1_powerups:
            powerup.collected = False
        for powerup in level2_powerups:
            powerup.collected = False
        for powerup in level3_powerups:
            powerup.collected = False

    # Reset stats
    game_stats['total_collected'] = 0
    game_stats['total_collectibles'] = get_level_collectibles_count(current_level)
    game_stats['lives'] = game_stats['max_lives']
    enemy_damage_cooldown = 0

    game_stats['level_start_ticks'] = pygame.time.get_ticks()
    game_stats['level_time_seconds'] = 0
    game_stats['level_score'] = 0

    game_stats["run_saved"] = False

def reset_game():
    """
    Återställ spelet till startläge (Level 1).
    Används när spelet startar från huvudmenyn.
    """
    global player, bg_manager, enemy_damage_cooldown, current_level
    current_level = 1  # Reset to Level 1
    player = Player(PLAYER_START_X, PLAYER_START_Y, max_jumps=1)  # Level 1: single jump
    bg_manager = BackgroundManager(WIDTH, HEIGHT, "level1")
    switch_music(LEVEL1_MUSIC)  # Switch to Level 1 music

    # Reset all collectibles
    for screen_collectibles in all_screen_collectibles:
        for collectible in screen_collectibles:
            collectible.collected = False

    # Reset all power-ups
    for powerup in level1_powerups:
        powerup.collected = False
    for powerup in level2_powerups:
        powerup.collected = False

    game_stats['total_collected'] = 0
    game_stats['total_collectibles'] = get_level_collectibles_count(1)  # Level 1 count
    game_stats['lives'] = game_stats['max_lives']
    enemy_damage_cooldown = 0

    game_stats['level_start_ticks'] = pygame.time.get_ticks()
    game_stats['level_time_seconds'] = 0
    game_stats['level_score'] = 0


def respawn_player():
    """
    Respawn player at start position after falling.
    Loses a life. Respawns at the start of the current level.
    """
    global player, bg_manager, boss_octosaucer, boss_camera, boss_victory_delay

    # Determine respawn screen and jump count based on current level
    if current_level == 1:
        respawn_screen = 0
        max_jumps = 1  # Level 1: single jump
    elif current_level == 2:
        respawn_screen = 3
        max_jumps = 2  # Level 2: double jump
    else:  # Level 3
        respawn_screen = 8  # Respawn i början av Level 3
        max_jumps = 2  # Level 3: double jump
        # Reset boss and camera for Level 3
        boss_octosaucer = None
        boss_camera = None
        boss_victory_delay = 0

    player = Player(PLAYER_START_X, PLAYER_START_Y, max_jumps=max_jumps)
    bg_manager.current_index = respawn_screen
    game_stats['lives'] -= 1
    # Note: player.has_hat is False in new Player instance (hat lost on death)


def start_level_2():
    """
    Transition from Level 1 to Level 2.
    Lives carry over, but collectible counter resets for new level.
    """
    global player, bg_manager, current_level
    current_level = 2
    player = Player(PLAYER_START_X, PLAYER_START_Y, max_jumps=2)  # Level 2: double jump
    bg_manager = BackgroundManager(WIDTH, HEIGHT, "level2")
    bg_manager.current_index = 3  # CRITICAL: Start at screen 3 (Level 2's first screen)
    switch_music(LEVEL2_MUSIC)  # Switch to Level 2 music
    # Reset collectible counter for Level 2
    game_stats['total_collected'] = 0
    game_stats['total_collectibles'] = get_level_collectibles_count(2)  # Level 2 count
    # Lives carry over (no reset)
    # Fedora resets (player.has_hat already False on new Player instance)

def finalize_level_score(level):
    elapsed_seconds = (pygame.time.get_ticks() - game_stats['level_start_ticks']) // 1000
    game_stats['level_time_seconds'] = int(elapsed_seconds)

    mushrooms = game_stats['total_collected']
    lives_left = game_stats['lives']

    target_time = 75 if level == 1 else 120
    time_bonus = max(0, (target_time - elapsed_seconds) * 10)

    level_score = mushrooms * 100 + lives_left * 250 + time_bonus

    game_stats['level_score'] = int(level_score)
    game_stats['total_score'] += int(level_score)

def unlock_level_2():
    """
    Unlock Level 2 in the level select menu.
    Called when Level 1 is completed.
    """
    global level2_unlocked
    level2_unlocked = True

def start_level_3():
    """
    Övergång från Level 2 till Level 3 (Boss Fight).
    Liv bärs över, collectible counter återställs.
    """
    global player, bg_manager, current_level, boss_octosaucer, boss_camera, boss_victory_delay
    current_level = 3
    player = Player(PLAYER_START_X, PLAYER_START_Y, max_jumps=2)  # Level 3: double jump
    bg_manager = BackgroundManager(WIDTH, HEIGHT, "level3")
    bg_manager.current_index = 8  # KRITISKT: Börja på screen 8 (Level 3 första screen)
    switch_music(LEVEL3_MUSIC)  # Byt till boss-musik

    # Återställ collectible counter för Level 3
    game_stats['total_collected'] = 0
    game_stats['total_collectibles'] = get_level_collectibles_count(3)

    # Boss skapas senare när spelaren når screen 9
    boss_octosaucer = None
    boss_camera = None
    boss_victory_delay = 0

def finalize_level_score(level):
    """
    Calculate score when a level is completed.
    Simple + stable formula (no chaos):
    - mushrooms: 100p each
    - remaining lives: 250p each
    - time bonus: if you beat target time, you get bonus
    """
    # Time in seconds since level start
    elapsed_seconds = (pygame.time.get_ticks() - game_stats['level_start_ticks']) // 1000
    game_stats['level_time_seconds'] = int(elapsed_seconds)

    mushrooms = game_stats['total_collected']
    lives_left = game_stats['lives']

    # Targets
    target_time = 75 if level == 1 else 120  # seconds
    time_bonus = max(0, (target_time - elapsed_seconds) * 10)

    level_score = mushrooms * 100 + lives_left * 250 + time_bonus

    game_stats['level_score'] = int(level_score)
    game_stats['total_score'] += int(level_score)

def draw_level1_popup(screen):
    """Rita instruktionspopup för level 1, screen 0."""
    # Visa bara på level 1, screen 0 (första bilden)
    if current_level != 1 or bg_manager.current_index != 0:
        return
    
    popup_x = 30
    popup_y = 80
    
    # Skapa popup
    popup = pygame.Surface((450, 280), pygame.SRCALPHA)
    pygame.draw.rect(popup, (30, 30, 40), (0, 0, 450, 280), border_radius=12)
    pygame.draw.rect(popup, (0, 140, 255), (0, 0, 450, 280), width=3, border_radius=12)
    
    # Fonts
    font_title = pygame.font.SysFont("bahnschrift", 32, bold=True)
    font_key = pygame.font.SysFont("bahnschrift", 24, bold=True)
    font_text = pygame.font.SysFont("bahnschrift", 22)
    
    # Titel
    title = font_title.render("Kontroller", True, (255, 255, 255))
    popup.blit(font_title.render("Kontroller", True, (0, 0, 0)), (22, 17))
    popup.blit(title, (20, 15))
    
    # Instruktioner
    y = 60
    instructions = [
        ("W", "Hoppa"),
        ("A", "Vänster"),
        ("D", "Höger"),
        ("S", "Ducka"),
        ("SPACE", "Hoppa (alternativ)"),
        ("", ""),
        ("2x SPACE", "Dubbelhopp (Aktiveras i Lvl 2)")
    ]
    
    for key, desc in instructions:
        if key:
            key_shadow = font_key.render(key, True, (0, 0, 0))
            key_surf = font_key.render(key, True, (0, 200, 255))
            popup.blit(key_shadow, (22, y + 2))
            popup.blit(key_surf, (20, y))
            popup.blit(font_text.render(desc, True, (0, 0, 0)), (152, y + 4))
            popup.blit(font_text.render(desc, True, (255, 255, 255)), (150, y + 2))
        y += 32
    
    screen.blit(popup, (popup_x, popup_y))


def draw_hud(screen):
    WHITE = (255, 255, 255)
    SHADOW = (0, 0, 0)

    # Fonts
    font_small = pygame.font.SysFont("bahnschrift", 28, bold=True)
    font_medium = pygame.font.SysFont("bahnschrift", 34, bold=True)

    # =========================
    # LEFT – MUSHROOM COUNTER
    # =========================
    icon_x = 24
    icon_y = 22
    screen.blit(hud_mushroom_icon, (icon_x, icon_y))

    mush_text = f"{game_stats['total_collected']} / {game_stats['total_collectibles']}"
    mush_shadow = font_small.render(mush_text, True, SHADOW)
    mush_surf = font_small.render(mush_text, True, WHITE)

    screen.blit(mush_shadow, (icon_x + 54, icon_y + 4))
    screen.blit(mush_surf, (icon_x + 52, icon_y + 2))

    # =========================
    # CENTER – SCORE & TIME
    # =========================
    elapsed_seconds = (pygame.time.get_ticks() - game_stats['level_start_ticks']) // 1000

    score_text = f"SCORE {game_stats['total_score']}"
    time_text = f"TIME {elapsed_seconds}s"

    score_shadow = font_medium.render(score_text, True, SHADOW)
    score_surf = font_medium.render(score_text, True, WHITE)

    time_shadow = font_small.render(time_text, True, SHADOW)
    time_surf = font_small.render(time_text, True, WHITE)

    center_x = WIDTH // 2

    screen.blit(score_shadow, (center_x - score_shadow.get_width() // 2 + 2, 22 + 2))
    screen.blit(score_surf, (center_x - score_surf.get_width() // 2, 22))

    screen.blit(time_shadow, (center_x - time_shadow.get_width() // 2 + 2, 62 + 2))
    screen.blit(time_surf, (center_x - time_surf.get_width() // 2, 62))

    # =========================
    # RIGHT – HEARTS (LIVES)
    # =========================
    max_lives = game_stats['max_lives']
    current_lives = game_stats['lives']

    heart_size = 40
    spacing = 10

    total_width = max_lives * heart_size + (max_lives - 1) * spacing
    start_x = WIDTH - total_width - 24
    heart_y = 20

    for i in range(max_lives):
        x = start_x + i * (heart_size + spacing)

        if i < current_lives:
            heart_img = pygame.transform.scale(hud_heart_full, (heart_size, heart_size))
        else:
            heart_img = pygame.transform.scale(hud_heart_empty, (heart_size, heart_size))

        screen.blit(heart_img, (x, heart_y))

# ============================================================================
# MAIN GAME LOOP
# ============================================================================
# Spel-loopen är hjärtat i spelet - den körs 60 gånger per sekund (60 FPS)
# och hanterar events, uppdaterar speltillstånd och ritar allt på skärmen.

running = True
while running:
    # ------------------------------------------------------------------------
    # EVENT HANTERING
    # ------------------------------------------------------------------------
    # Hantera alla events som inträffat sedan förra framen
    # (tangentryckningar, musklick, stänga fönster etc.)
    for event in pygame.event.get():
        # Kryss-knapp i fönstret - avsluta spelet
        if event.type == pygame.QUIT:
            running = False

        # KEYDOWN events (när tangent trycks NER - inte kontinuerligt!)
        # Används för engångs-actions som hopp och pausa
        if event.type == pygame.KEYDOWN:
            # ESC-tangent: Pausa/återuppta spelet
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    game_state = "paused"  # Pausa spelet
                elif game_state == "paused":
                    game_state = "playing"  # Återuppta spelet

            # Hopp med SPACE, W eller Uppåtpil (EXAKT som test.py line 175)
            # Event-baserad input = tryck EN gång för att hoppa
            # Spelaren kan inte hoppa igen förrän hen landar (on_ground = True)
            elif game_state == "playing" and (event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w):
                player.jump()


        # Hantera meny-klick baserat på nuvarande speltillstånd
        # Menyerna returnerar "start", "quit", "resume" eller None
        if game_state == "main_menu":
            action = main_menu.handle_events(event)
            if action == "start":
                game_state = "playing"  # Starta spelet
            elif action == "levels":
                game_state = "level_select"  # Öppna level select-menyn
            elif action == "scores":
                game_state = "scores"  # Öppna high scores-menyn
            elif action == "quit":
                running = False  # Avsluta spelet

        elif game_state == "scores":
            action = scores_menu.handle_events(event)
            if action == "back":
                game_state = "main_menu"
                if action == "back":
                    game_state = "main_menu"

        elif game_state == "paused":
            action = pause_menu.handle_events(event)
            if action == "resume":
                game_state = "playing"  # Återuppta spelet
            elif action == "main_menu":
                reset_game()
                switch_music(MENU_MUSIC)
                game_state = "main_menu"  # Återgå till huvudmenyn
            elif action == "settings":
                game_state = "settings"


        elif game_state == "game_over":
            action = game_over_menu.handle_events(event)
            if action == "restart":
                restart_current_level()  # Restart current level (not back to Level 1!)
                game_state = "playing"  # Starta om spelet
            elif action == "main_menu":
                reset_game()  # Återställ spelet
                switch_music(MENU_MUSIC)  # Switch to menu music
                game_state = "main_menu"  # Återgå till huvudmenyn

        elif game_state == "victory":
            action = victory_menu.handle_events(event)
            if action == "main_menu":
                reset_game()  # Återställ spelet
                switch_music(MENU_MUSIC)  # Switch to menu music
                game_state = "main_menu"  # Återgå till huvudmenyn

        elif game_state == "level_select":
            action = level_select_menu.handle_events(event, level2_unlocked)
            if action == "start_level_1":
                reset_game()  # Reset to Level 1
                game_state = "playing"
            elif action == "start_level_2":
                if level2_unlocked:
                    start_level_2()
                    game_state = "playing"
            elif action == "start_level_3":
                # Level 3 (Boss Fight) - alltid upplåst för testning
                start_level_3()
                game_state = "playing"
            elif action == "back":
                game_state = "main_menu"

        elif game_state == "scores":
            action = scores_menu.handle_events(event)
            if action == "back":
                game_state = "main_menu"

        elif game_state == "settings":
            action = settings_menu.handle_events(event)
            if action == "back":
                game_state = "paused"  # Återgå till pausmenyn

    # ------------------------------------------------------------------------
    # UPDATE & RENDER (baserat på speltillstånd)
    # ------------------------------------------------------------------------

    # Olika logik körs beroende på om vi är i menyn, spelar eller är pausad

    if game_state == "main_menu":
        # HUVUDMENY STATE
        # Rita bara huvudmenyn, inget spel körs
        main_menu.draw(screen, particle_manager)

    elif game_state == "playing":
        # SPEL STATE
        # Get current screen obstacles and collectibles
        current_obstacles = all_screen_obstacles[bg_manager.current_index]
        current_collectibles = all_screen_collectibles[bg_manager.current_index]

        # 1. Uppdatera spellogik (fysik, kollisioner, input)
        player.update(current_obstacles, WIDTH, HEIGHT)

        # 1.5. Uppdatera bakgrund baserat på spelarens position
        # Kolla om boss är aktiv för att låsa arenan
        boss_active = (current_level == 3 and
                       bg_manager.current_index == 9 and
                       boss_octosaucer is not None and
                       boss_octosaucer.state != boss_octosaucer.STATE_DEATH)
        bg_manager.update_for_player(player, boss_active=boss_active)

        # 1.6. Aktivera/deaktivera fienden beroende på bana
        # DISABLE enemies during Level 3 (boss fight level)
        if current_level != 3 and bg_manager.current_index >= ENEMY_ACTIVE_FROM_SCREEN:
            # Add both enemies if not already in group
            if enemy_bottom not in enemy_group:
                enemy_group.add(enemy_bottom)
            if enemy_top not in enemy_group:
                enemy_group.add(enemy_top)
        else:
            # Remove both enemies if in group
            if enemy_bottom in enemy_group:
                enemy_group.remove(enemy_bottom)
            if enemy_top in enemy_group:
                enemy_group.remove(enemy_top)

        # 1.7. Uppdatera fienden (om gruppen är tom händer inget)
        enemy_group.update(current_obstacles, WIDTH, HEIGHT)

        # 1.7.1. Check enemy-player collision (damage + bounce)
        # Uppdatera cooldown
        if enemy_damage_cooldown > 0:
            enemy_damage_cooldown -= 1

        for enemy in enemy_group:
            if enemy.rect.colliderect(player.rect):
                # Skada spelaren (1 liv) om cooldown är klar
                if enemy_damage_cooldown == 0 and game_stats['lives'] > 0:
                    game_stats['lives'] -= 1
                    enemy_damage_cooldown = ENEMY_DAMAGE_COOLDOWN_TIME
                    hit_sound.play()
                    # Om inga liv kvar, game over
                    if game_stats['lives'] <= 0:
                        game_state['lives'] = 0

                        if not game_stats.get("run_saved", False):
                            add_score(game_stats.get("total_score", 0))
                            game_stats["run_saved"] = True
                        game_state = "game_over"

                # Studsa fienden från spelaren
                # Beräkna kollisionsriktning
                dx = enemy.rect.centerx - player.rect.centerx
                dy = enemy.rect.centery - player.rect.centery

                # Byt riktning baserat på var kollisionen sker
                if abs(dx) > abs(dy):  # Horisontell kollision
                    enemy.speed_x = -enemy.speed_x
                else:  # Vertikal kollision
                    enemy.speed_y = -enemy.speed_y

                # Flytta fienden bort från spelaren för att undvika att fastna
                if dx > 0:
                    enemy.rect.left = player.rect.right
                else:
                    enemy.rect.right = player.rect.left
                if dy > 0:
                    enemy.rect.top = player.rect.bottom
                else:
                    enemy.rect.bottom = player.rect.top

        # 1.7.2. Update and check flying enemies (Level 2 only)
        if current_level == 2 and bg_manager.current_index in level2_flying_enemies:
            current_flying_enemies = level2_flying_enemies[bg_manager.current_index]

            for flying_enemy in current_flying_enemies:
                # Update flying enemy
                flying_enemy.update(player, WIDTH, HEIGHT)

                # Check collision with player
                if flying_enemy.rect.colliderect(player.rect):
                    # Damage player if cooldown is ready
                    if enemy_damage_cooldown == 0 and game_stats['lives'] > 0:
                        game_stats['lives'] -= 1
                        enemy_damage_cooldown = ENEMY_DAMAGE_COOLDOWN_TIME
                        # Game over if no lives left
                        if game_stats['lives'] <= 0:
                            game_state = "game_over"

        # 1.7.3. Boss Arena Logic (Level 3, Screen 9)
        if current_level == 3 and bg_manager.current_index == 9:
            # Initiera boss och camera om inte redan skapad
            if boss_octosaucer is None:
                from boss_octosaucer import BossOctosaucer
                from camera import Camera

                sprites_dir = os.path.join(base_dir, "..", "assets", "sprites")
                boss_image_path = os.path.join(sprites_dir, "enemies", "enemy_boss.png")
                boss_octosaucer = BossOctosaucer(810, 350, boss_image_path)  # Centrerad och lägre för att kunna nås

                # Skapa kamera för zoom-effekt (0.7 = visar mer av banan)
                boss_camera = Camera(WIDTH, HEIGHT, zoom_level=0.7)

            # Screen shake callback
            def trigger_screen_shake():
                """Callback för screen shake vid tentacle slam"""
                global screen_shake_timer
                screen_shake_timer = 20  # 20 frames shake

            # Uppdatera boss
            boss_result = boss_octosaucer.update(player, trigger_screen_shake)

            # Hantera boss damage till spelare (från attacker)
            if boss_result and 'player_damage' in boss_result:
                if enemy_damage_cooldown == 0 and game_stats['lives'] > 0:
                    game_stats['lives'] -= boss_result['player_damage']
                    enemy_damage_cooldown = ENEMY_DAMAGE_COOLDOWN_TIME
                    if game_stats['lives'] <= 0:
                        game_state = "game_over"

            # Kolla spelaren-boss kollision (jump-on-boss damage)
            if boss_octosaucer.state != boss_octosaucer.STATE_DEATH:
                collision_result = boss_octosaucer.check_player_jump_damage(player)

                if collision_result:
                    if 'boss_damage' in collision_result:
                        # Framgångsrikt hopp - skada boss och studsa spelaren
                        boss_octosaucer.take_damage(collision_result['boss_damage'])
                        player.vel_y = collision_result['player_bounce']
                    elif 'player_damage' in collision_result:
                        # Kollision från sida/underifrån - skada spelare
                        if enemy_damage_cooldown == 0 and game_stats['lives'] > 0:
                            game_stats['lives'] -= collision_result['player_damage']
                            enemy_damage_cooldown = ENEMY_DAMAGE_COOLDOWN_TIME
                            if game_stats['lives'] <= 0:
                                game_state = "game_over"

            # Kolla om boss är besegrad
            if boss_result and 'boss_defeated' in boss_result:
                # Starta victory delay timer om inte redan startad
                if boss_victory_delay == 0:
                    boss_victory_delay = 240  # 4 sekunder (60 FPS * 4) för att spela boss death sound
                    boss_death_sound.play()  # Spela boss death sound

        # Boss victory delay countdown (after boss defeated)
        if boss_victory_delay > 0:
            boss_victory_delay -= 1

            # När delay är klar, övergång till victory screen (Screen 10)
            if boss_victory_delay == 0:
                bg_manager.current_index = 10
                player.x = WIDTH // 2  # Centrera spelaren
                boss_octosaucer = None
                boss_camera = None

        # 1.8. Check if player fell off the screen (DEATH!)
        if player.rect.y > DEATH_ZONE_Y:
            if game_stats['lives'] > 1:
                # Still have lives left - respawn at start
                respawn_player()
            else:
                # No lives left - game over
                game_stats['lives'] = 0
                game_state = "game_over"

        # 1.9. Check collectible collisions
        for collectible in current_collectibles:
            if collectible.check_collision(player.rect):
                game_stats['total_collected'] += 1
                coin_sound.play()

                if game_stats['total_collected'] % 3 == 0:
                    special_coin_sound.play()


        # 1.9.5. Check power-up collisions
        if current_level == 1:
            powerups_to_check = level1_powerups
        elif current_level == 2:
            powerups_to_check = level2_powerups
        else:  # Level 3
            powerups_to_check = level3_powerups
        for powerup in powerups_to_check:
                if not powerup.collected and powerup.check_collision(player.rect):
                    # Grant fedora effects
                    if current_level in [1, 2, 3]:  # Alla nivåer kan få fedora
                        player.has_hat = True
                        game_stats['lives'] += 1
                        powerup.collected = True

        # 1.10. Check for VICTORY! (reached final platform)
        # Level 1 Victory Check - Transition to Level 2
        if current_level == 1 and bg_manager.current_index == LEVEL_1_FINAL_SCREEN:
            # Final platform: screen2_obstacles[16] = Obstacle(1820, 950, 110, 50)
            # Last mushroom at x=1845
            final_platform_x = 1820
            final_platform_y = 950
            final_platform_width = 110
            player_center_x = player.rect.centerx

            # Victory zone: anywhere on the platform (player just needs to land on it)
            if (final_platform_x <= player_center_x <= final_platform_x + final_platform_width and
                final_platform_y - 10 <= player.rect.bottom <= final_platform_y + 20):
                # Level 1 complete - unlock Level 2 and show victory
                unlock_level_2()
                finalize_level_score(1)
                
                # Save score when Level 1 is completed
                if not game_stats.get("run_saved", False):
                    add_score(game_stats.get("total_score", 0))
                    game_stats["run_saved"] = True
                
                game_state = "victory"


        # Level 2 Victory Check - Transition to Level 3
        elif current_level == 2 and bg_manager.current_index == LEVEL_2_FINAL_SCREEN:
            # Final platform: screen7_obstacles[18] = Obstacle(1820, 950, 90, 50, "cloud")
            # Last mushroom at x=1870
            final_platform_x = 1820
            final_platform_y = 950
            final_platform_width = 90
            player_center_x = player.rect.centerx

            # Victory zone: anywhere on the platform (player just needs to land on it)
            if (final_platform_x <= player_center_x <= final_platform_x + final_platform_width and
                final_platform_y - 10 <= player.rect.bottom <= final_platform_y + 20):
                # Level 2 complete! Transition to Level 3 (Boss Fight)
                finalize_level_score(2)
                
                # Save score when Level 2 is completed
                if not game_stats.get("run_saved", False):
                    add_score(game_stats.get("total_score", 0))
                    game_stats["run_saved"] = True
                
                start_level_3()

        # Level 3 Victory Check - Game Complete!
        elif current_level == 3 and bg_manager.current_index == LEVEL_3_FINAL_SCREEN:
            # Victory screen (Screen 10) - auto-transition efter 3 sekunder
            if not hasattr(player, 'victory_timer'):
                player.victory_timer = 180  # 3 sekunder (60 FPS * 3)

            player.victory_timer -= 1

            if player.victory_timer == 0:
                # Spelet klart! Visa final victory
                finalize_level_score(3)
                
                if not game_stats.get("run_saved", False):
                    add_score(game_stats.get("total_score", 0))
                    game_stats["run_saved"] = True
                game_state = "victory"

        # 2. Rita allt (bakgrund -> hinder -> collectibles -> spelare -> fiende -> HUD)

        # === Boss Arena Rendering med Camera Zoom (Screen 9) ===
        if current_level == 3 and bg_manager.current_index == 9 and boss_camera is not None:
            # Beräkna screen shake offset först
            shake_offset_x = 0
            shake_offset_y = 0
            if screen_shake_timer > 0:
                shake_offset_x = random.randint(-screen_shake_intensity, screen_shake_intensity)
                shake_offset_y = random.randint(-screen_shake_intensity, screen_shake_intensity)
                screen_shake_timer -= 1

            # Rita bakgrund normalt (fullscreen)
            bg_manager.draw(screen)
            particle_manager.update_and_draw(screen)

            # Rita alla hinder/plattformar med zoom-transformation
            for obstacle in current_obstacles:
                # Transformera rect för zoom
                zoomed_rect = boss_camera.transform_rect(obstacle.rect)
                # Skapa en skalad version av image (obstacles use .image, not .sprite)
                if hasattr(obstacle, 'image') and obstacle.image:
                    zoomed_image = boss_camera.transform_surface(obstacle.image)
                    screen.blit(zoomed_image, (zoomed_rect.x + shake_offset_x, zoomed_rect.y + shake_offset_y))
                else:
                    # Rita som färgad rektangel (fallback)
                    shaken_rect = zoomed_rect.move(shake_offset_x, shake_offset_y)
                    pygame.draw.rect(screen, obstacle.color if hasattr(obstacle, 'color') else (100, 100, 100), shaken_rect)

            # Rita spelaren med zoom-transformation
            zoomed_player_image = boss_camera.transform_surface(player.current_image)
            # Använd samma offset-logik som player.draw()
            image_rect = zoomed_player_image.get_rect()
            player_pos = boss_camera.transform_pos(player.rect.centerx, player.rect.bottom + player.visual_offset)
            # Transformera visual offset också
            zoomed_visual_offset = int(player.visual_offset * boss_camera.zoom_level)
            image_rect.centerx = player_pos[0] + shake_offset_x
            image_rect.bottom = player_pos[1] + shake_offset_y
            screen.blit(zoomed_player_image, image_rect)

            # Rita boss med zoom-transformation
            if boss_octosaucer:
                # Hämta boss-bild med effekter
                boss_display_image = boss_octosaucer.get_display_image()
                if boss_display_image:
                    # Transformera boss image
                    zoomed_boss_image = boss_camera.transform_surface(boss_display_image)
                    boss_pos = boss_camera.transform_pos(boss_octosaucer.rect.x, boss_octosaucer.rect.y)
                    screen.blit(zoomed_boss_image, (boss_pos[0] + shake_offset_x, boss_pos[1] + shake_offset_y))

                # Rita HP bar (också zoomad)
                bar_width = 300
                bar_height = 20
                bar_x = boss_octosaucer.rect.centerx - bar_width // 2
                bar_y = boss_octosaucer.rect.top - 40

                # Transformera HP bar position och storlek
                zoomed_bar_pos = boss_camera.transform_pos(bar_x, bar_y)
                zoomed_bar_size = boss_camera.transform_size(bar_width, bar_height)

                # Bakgrund (svart)
                bg_rect = pygame.Rect(zoomed_bar_pos[0] + shake_offset_x, zoomed_bar_pos[1] + shake_offset_y, zoomed_bar_size[0], zoomed_bar_size[1])
                pygame.draw.rect(screen, (0, 0, 0), bg_rect)

                # HP (färgad baserat på HP)
                hp_percent = boss_octosaucer.hp / boss_octosaucer.max_hp
                hp_bar_width = int(zoomed_bar_size[0] * hp_percent)

                if hp_percent > 0.66:
                    hp_color = (0, 255, 0)
                elif hp_percent > 0.33:
                    hp_color = (255, 255, 0)
                else:
                    hp_color = (255, 0, 0)

                hp_rect = pygame.Rect(zoomed_bar_pos[0] + shake_offset_x, zoomed_bar_pos[1] + shake_offset_y, hp_bar_width, zoomed_bar_size[1])
                pygame.draw.rect(screen, hp_color, hp_rect)

                # Border
                pygame.draw.rect(screen, (255, 255, 255), bg_rect, 2)

                # HP text (skalad font)
                font_size = int(24 * boss_camera.zoom_level)
                if font_size > 0:
                    hp_font = pygame.font.Font(None, font_size)
                    hp_text = hp_font.render(f"{boss_octosaucer.hp}/{boss_octosaucer.max_hp}", True, (255, 255, 255))
                    text_rect = hp_text.get_rect(center=(bg_rect.centerx, bg_rect.centery))
                    screen.blit(hp_text, text_rect)

                # Rita boss attacker (zoomade)
                for hitbox in boss_octosaucer.active_hitboxes:
                    # Transformera hitbox position och storlek
                    zoomed_hitbox_rect = boss_camera.transform_rect(hitbox.rect)
                    shaken_rect = zoomed_hitbox_rect.move(shake_offset_x, shake_offset_y)

                    # Get the sprite image from the attack and render it
                    sprite_image = None
                    sprite_pos = None

                    # TentacleSlam - uses boss_crate.png
                    if hasattr(hitbox, 'crate_image'):
                        if hitbox.warning:
                            # Warning: faded crate at shadow position
                            sprite_image = pygame.transform.scale(hitbox.crate_image_faded, (shaken_rect.width, shaken_rect.height))
                            shadow_pos = boss_camera.transform_pos(hitbox.rect.x, hitbox.shadow_y)
                            sprite_pos = (shadow_pos[0] + shake_offset_x, shadow_pos[1] + shake_offset_y)
                        else:
                            # Attack: full opacity falling crate
                            sprite_image = pygame.transform.scale(hitbox.crate_image, (shaken_rect.width, shaken_rect.height))
                            sprite_pos = shaken_rect.topleft

                    # EyeBeam - uses laser-beams.png
                    elif hasattr(hitbox, 'laser_image'):
                        if hitbox.warning:
                            sprite_image = pygame.transform.scale(hitbox.laser_image_faded, (shaken_rect.width, shaken_rect.height))
                        else:
                            sprite_image = pygame.transform.scale(hitbox.laser_image, (shaken_rect.width, shaken_rect.height))
                        sprite_pos = shaken_rect.topleft

                    # ProjectileShot - uses fireorb.png
                    elif hasattr(hitbox, 'fireorb_image'):
                        sprite_image = pygame.transform.scale(hitbox.fireorb_image, (shaken_rect.width, shaken_rect.height))
                        sprite_pos = shaken_rect.topleft

                    # FastSweep - uses ufo.png
                    elif hasattr(hitbox, 'ufo_image_sweep'):
                        if hitbox.warning:
                            # Warning: pulsing faded UFO on screen edge
                            pulse_scale = 1.0 + 0.2 * math.sin(hitbox.lifetime * 0.3)
                            pulse_width = int(120 * pulse_scale * boss_camera.zoom_level)
                            pulse_height = int(90 * pulse_scale * boss_camera.zoom_level)
                            pulsed_ufo = pygame.transform.scale(hitbox.ufo_image_original, (pulse_width, pulse_height))
                            pulsed_ufo.set_alpha(128)

                            # Position on screen edge
                            if hitbox.direction > 0:
                                edge_pos = boss_camera.transform_pos(hitbox.warning_x, hitbox.rect.y + hitbox.rect.height // 2)
                                ufo_x = edge_pos[0] + shake_offset_x
                                ufo_y = edge_pos[1] + shake_offset_y - pulse_height // 2
                            else:
                                edge_pos = boss_camera.transform_pos(hitbox.warning_x + 80, hitbox.rect.y + hitbox.rect.height // 2)
                                ufo_x = edge_pos[0] + shake_offset_x - pulse_width
                                ufo_y = edge_pos[1] + shake_offset_y - pulse_height // 2

                            sprite_image = pulsed_ufo
                            sprite_pos = (ufo_x, ufo_y)
                        else:
                            # Attack: full opacity UFO sweeping
                            sprite_image = pygame.transform.scale(hitbox.ufo_image_sweep, (shaken_rect.width, shaken_rect.height))
                            sprite_pos = shaken_rect.topleft

                    # Blit the sprite if we have one
                    if sprite_image and sprite_pos:
                        screen.blit(sprite_image, sprite_pos)

                # Rita gravity pulls
                for pull in boss_octosaucer.active_gravity_pulls:
                    if pull.warning:
                        # Varnings-cirkel
                        pulse = int(50 + 20 * pygame.math.Vector2(0, 1).rotate(pull.lifetime * 0.2).y)
                        center_pos = boss_camera.transform_pos(pull.center_x, pull.center_y)
                        zoomed_pulse = int(pulse * boss_camera.zoom_level)
                        shaken_center = (center_pos[0] + shake_offset_x, center_pos[1] + shake_offset_y)
                        pygame.draw.circle(screen, (255, 255, 0), shaken_center, zoomed_pulse, 3)
                    else:
                        # Dragnings-effekt
                        center_pos = boss_camera.transform_pos(pull.center_x, pull.center_y)
                        shaken_center = (center_pos[0] + shake_offset_x, center_pos[1] + shake_offset_y)
                        zoomed_radius = int(pull.pull_radius * boss_camera.zoom_level)
                        for i in range(3):
                            radius = int(zoomed_radius * (1 - i * 0.3))
                            pygame.draw.circle(screen, pull.color, shaken_center, radius, 2)
                        # Centrum
                        pygame.draw.circle(screen, (255, 0, 0), shaken_center, int(20 * boss_camera.zoom_level))

            # Rita HUD normalt (inte zoomat)
            draw_hud(screen)
            if current_level == 1:
                draw_level1_popup(screen)

            # Rita instruktioner för boss fight
            if boss_octosaucer and boss_octosaucer.state != boss_octosaucer.STATE_DEATH:
                instruction_font = pygame.font.Font(None, 48)
                instruction_text = instruction_font.render("Jump on the boss's head to damage it!", True, (255, 255, 100))
                instruction_shadow = instruction_font.render("Jump on the boss's head to damage it!", True, (0, 0, 0))
                text_x = WIDTH // 2 - instruction_text.get_width() // 2
                text_y = 120
                screen.blit(instruction_shadow, (text_x + 2, text_y + 2))
                screen.blit(instruction_text, (text_x, text_y))

        # === Normal Rendering (alla andra screens) ===
        else:
            bg_manager.draw(screen)          # Bakgrund
            particle_manager.update_and_draw(screen)  # Partiklar framför bakgrund

            # Rita alla hinder/plattformar
            for obstacle in current_obstacles:
                obstacle.draw(screen)

            # Rita collectibles
            for collectible in current_collectibles:
                collectible.draw(screen)

            # Rita power-ups
            if current_level == 1:
                powerups_to_draw = level1_powerups
            elif current_level == 2:
                powerups_to_draw = level2_powerups
            else:  # Level 3
                powerups_to_draw = level3_powerups
            for powerup in powerups_to_draw:
                powerup.draw(screen)

            # Rita flying enemies (Level 2 only)
            if current_level == 2 and bg_manager.current_index in level2_flying_enemies:
                for flying_enemy in level2_flying_enemies[bg_manager.current_index]:
                    flying_enemy.draw(screen)

            # Rita spelaren
            player.draw(screen)

            # Rita fienden (om den är aktiv)
            enemy_group.draw(screen)

            # Rita HUD
            draw_hud(screen)
            if current_level == 1:
                draw_level1_popup(screen)

        # === Victory Screen Text (Screen 10) ===
        if current_level == 3 and bg_manager.current_index == 10:
                # Rita "VICTORY" text stor i mitten
                victory_font = pygame.font.Font(None, 200)
                victory_text = victory_font.render("VICTORY", True, (255, 215, 0))  # Guld färg
                victory_rect = victory_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))

                # Shadow för djup
                shadow_text = victory_font.render("VICTORY", True, (0, 0, 0))
                screen.blit(shadow_text, (victory_rect.x + 5, victory_rect.y + 5))
                screen.blit(victory_text, victory_rect)

    elif game_state == "paused":
        # PAUSED STATE
        # Rita spelet "fryst" i bakgrunden, sedan pausmenyn ovanpå
        current_obstacles = all_screen_obstacles[bg_manager.current_index]
        current_collectibles = all_screen_collectibles[bg_manager.current_index]

        # 1. Rita det frysta spelet (samma som "playing" men utan update)
        bg_manager.draw(screen)
        particle_manager.update_and_draw(screen)

        for obstacle in current_obstacles:
            obstacle.draw(screen)
        for collectible in current_collectibles:
            collectible.draw(screen)
        powerups_to_draw = level1_powerups if current_level == 1 else level2_powerups
        for powerup in powerups_to_draw:
                powerup.draw(screen)
        player.draw(screen)
        enemy_group.draw(screen)
        draw_hud(screen)

        # 2. Rita pausmenyn ovanpå det frysta spelet
        pause_menu.draw(screen)

    elif game_state == "settings":
        # SETTINGS STATE
        # Rita spelet "fryst" i bakgrunden, sedan settings-menyn ovanpå
        current_obstacles = all_screen_obstacles[bg_manager.current_index]
        current_collectibles = all_screen_collectibles[bg_manager.current_index]

        # 1. Rita det frysta spelet (samma som "playing" men utan update)
        bg_manager.draw(screen)
        particle_manager.update_and_draw(screen)

        for obstacle in current_obstacles:
            obstacle.draw(screen)
        for collectible in current_collectibles:
            collectible.draw(screen)
        powerups_to_draw = level1_powerups if current_level == 1 else level2_powerups
        for powerup in powerups_to_draw:
            powerup.draw(screen)
        player.draw(screen)
        enemy_group.draw(screen)
        draw_hud(screen)

        # 2. Rita settings-menyn ovanpå det frysta spelet
        settings_menu.draw(screen)

        # 3. Uppdatera sliders för realtidsvolymkontroll
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        settings_menu.update(mouse_pos, mouse_pressed)

    elif game_state == "game_over":
        # GAME OVER STATE
        # Rita spelet "fryst" i bakgrunden, sedan game over-skärmen ovanpå
        current_obstacles = all_screen_obstacles[bg_manager.current_index]
        current_collectibles = all_screen_collectibles[bg_manager.current_index]

        bg_manager.draw(screen)
        particle_manager.update_and_draw(screen)

        for obstacle in current_obstacles:
            obstacle.draw(screen)
        for collectible in current_collectibles:
            collectible.draw(screen)
        powerups_to_draw = level1_powerups if current_level == 1 else level2_powerups
        for powerup in powerups_to_draw:
                powerup.draw(screen)
        player.draw(screen)
        enemy_group.draw(screen)
        draw_hud(screen)

        # Rita game over-skärmen ovanpå det frysta spelet
        game_over_menu.draw(screen)

    elif game_state == "victory":
        # VICTORY STATE
        # Rita spelet "fryst" i bakgrunden, sedan victory-skärmen ovanpå
        current_obstacles = all_screen_obstacles[bg_manager.current_index]
        current_collectibles = all_screen_collectibles[bg_manager.current_index]

        bg_manager.draw(screen)
        particle_manager.update_and_draw(screen)

        for obstacle in current_obstacles:
            obstacle.draw(screen)
        for collectible in current_collectibles:
            collectible.draw(screen)
        powerups_to_draw = level1_powerups if current_level == 1 else level2_powerups
        for powerup in powerups_to_draw:
                powerup.draw(screen)
        player.draw(screen)
        enemy_group.draw(screen)
        draw_hud(screen)

        # Rita victory-skärmen ovanpå det frysta spelet
        victory_menu.draw(
            screen,
            game_stats['total_collected'],
            game_stats['total_collectibles'],
            game_stats['level_score'],
            game_stats['total_score'],
            game_stats['level_time_seconds']
    )
        
    elif game_state == "scores":
        scores_menu.draw(screen, particle_manager)

    elif game_state == "level_select":
        # LEVEL SELECT STATE
        # Rita level select-menyn
        level_select_menu.draw(screen, level2_unlocked)

    # ------------------------------------------------------------------------
    # DISPLAY UPDATE & FRAMERATE
    # ------------------------------------------------------------------------
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

import pygame
import os
from scores import get_last_scores, get_high_score

# ============================================================================
# BUTTON CLASS (oförändrad)
# ============================================================================
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color

    def draw(self, screen, font):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=8)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color

    def is_clicked(self, mouse_pos, mouse_pressed):
        return mouse_pressed and self.rect.collidepoint(mouse_pos)


# ============================================================================
# SLIDER CLASS
# ============================================================================
class Slider:
    def __init__(self, x, y, width, height, min_val=0.0, max_val=1.0, initial_val=0.5):
        """
        Horizontal slider for volume control.

        Args:
            x, y: Top-left position of slider
            width, height: Dimensions of slider bar
            min_val, max_val: Value range (0.0 to 1.0 for volume)
            initial_val: Starting value
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val

        # Visual properties
        self.bar_color = (60, 60, 70)
        self.fill_color = (0, 140, 255)
        self.handle_color = (255, 255, 255)
        self.handle_hover_color = (200, 200, 200)

        # Handle dimensions
        self.handle_width = 20
        self.handle_height = height + 10  # Slightly taller than bar

        # Interaction state
        self.dragging = False
        self.hovering = False

    def get_handle_rect(self):
        """Calculate handle position based on current value."""
        # Value as percentage of range
        percentage = (self.value - self.min_val) / (self.max_val - self.min_val)
        # Handle X position (centered on value position)
        handle_x = self.rect.x + int(percentage * self.rect.width) - self.handle_width // 2
        handle_y = self.rect.y - 5  # Center vertically on bar
        return pygame.Rect(handle_x, handle_y, self.handle_width, self.handle_height)

    def update(self, mouse_pos, mouse_pressed):
        """
        Update slider state based on mouse interaction.
        Returns True if value changed.
        """
        handle_rect = self.get_handle_rect()
        old_value = self.value

        # Check hover
        self.hovering = handle_rect.collidepoint(mouse_pos)

        # Start dragging
        if mouse_pressed and (self.hovering or self.dragging):
            self.dragging = True

        # Update value while dragging
        if self.dragging and mouse_pressed:
            # Clamp mouse X to slider bounds
            relative_x = max(0, min(mouse_pos[0] - self.rect.x, self.rect.width))
            percentage = relative_x / self.rect.width
            self.value = self.min_val + percentage * (self.max_val - self.min_val)
            self.value = max(self.min_val, min(self.max_val, self.value))

        # Stop dragging
        if not mouse_pressed:
            self.dragging = False

        return old_value != self.value

    def draw(self, screen, font, label):
        """Draw slider with label and value percentage."""
        # Label text
        label_surface = font.render(label, True, (255, 255, 255))
        screen.blit(label_surface, (self.rect.x, self.rect.y - 40))

        # Slider bar background
        pygame.draw.rect(screen, self.bar_color, self.rect, border_radius=4)

        # Filled portion (left side up to handle)
        percentage = (self.value - self.min_val) / (self.max_val - self.min_val)
        fill_width = int(percentage * self.rect.width)
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
            pygame.draw.rect(screen, self.fill_color, fill_rect, border_radius=4)

        # Handle
        handle_rect = self.get_handle_rect()
        handle_color = self.handle_hover_color if self.hovering or self.dragging else self.handle_color
        pygame.draw.rect(screen, handle_color, handle_rect, border_radius=6)
        pygame.draw.rect(screen, (0, 0, 0), handle_rect, width=2, border_radius=6)  # Border

        # Value percentage text
        value_text = f"{int(self.value * 100)}%"
        value_surface = font.render(value_text, True, (255, 255, 255))
        screen.blit(value_surface, (self.rect.x + self.rect.width + 20, self.rect.y - 5))


# ============================================================================
# MAIN MENU (modifierad för partiklar)
# ============================================================================
class MainMenu:
    def __init__(self, width, height, background_path):
        self.width = width
        self.height = height

        # Bakgrund
        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale(self.background, (width, height))

        # Fonts
        self.font_large = pygame.font.Font(None, 130)
        self.font_medium = pygame.font.Font(None, 64)

        # Buttons
        button_width = 320
        button_height = 72
        spacing = 20

        total_height = button_height * 4 + spacing * 3
        start_y = height // 2 - total_height // 2
        center_x = width // 2 - button_width // 2

        self.start_button = Button(
            center_x, start_y,
            button_width, button_height,
            "Start", (0, 140, 0), (0, 190, 0)
        )

        self.levels_button = Button(
            center_x, start_y + (button_height + spacing),
            button_width, button_height,
            "Levels", (110, 60, 190), (150, 90, 230)
        )

        self.scores_button = Button(
            center_x, start_y + 2 * (button_height + spacing),
            button_width, button_height,
            "Scores", (230, 140, 0), (255, 180, 40)
        )

        self.quit_button = Button(
            center_x, start_y + 3 * (button_height + spacing),
            button_width, button_height,
            "Quit", (150, 0, 0), (200, 0, 0)
        )

    # 🔥 MODIFIERAD för partiklar i menyn
    def draw(self, screen, particle_manager=None):
        # Bakgrund
        screen.blit(self.background, (0, 0))

        # Partiklar i huvudmenyn
        if particle_manager:
            particle_manager.update_and_draw(screen)

        # Title text + shadow
        shadow = self.font_large.render("PEPE'S TRIP", True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(self.width // 2 + 3, 180 + 3))
        screen.blit(shadow, shadow_rect)

        # --- Stylized title: PEPE'S TRIP ---

        title_text = "PEPE'S TRIP"
        center_x = self.width // 2
        center_y = 170

        # 1. Soft glow (bakom)
        for offset in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            glow = self.font_large.render(title_text, True, (255, 180, 80))
            glow_rect = glow.get_rect(center=(center_x + offset[0], center_y + offset[1]))
            screen.blit(glow, glow_rect)

        # 2. Shadow (djup)
        shadow = self.font_large.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow.get_rect(center=(center_x + 3, center_y + 3))
        screen.blit(shadow, shadow_rect)

        # 3. Main title
        title = self.font_large.render(title_text, True, (255, 245, 220))
        title_rect = title.get_rect(center=(center_x, center_y))
        screen.blit(title, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        # Hover-effekter
        self.start_button.check_hover(mouse_pos)
        self.levels_button.check_hover(mouse_pos)
        self.scores_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)

        # Rita knappar
        self.start_button.draw(screen, self.font_medium)
        self.levels_button.draw(screen, self.font_medium)
        self.scores_button.draw(screen, self.font_medium)
        self.quit_button.draw(screen, self.font_medium)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.start_button.is_clicked(mouse_pos, True):
                return "start"
            if self.levels_button.is_clicked(mouse_pos, True):
                return "levels"
            if self.scores_button.is_clicked(mouse_pos, True):
                return "scores"
            if self.quit_button.is_clicked(mouse_pos, True):
                return "quit"
        return None


# ============================================================================
# PAUSE MENU
# ============================================================================
class PauseMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font_large = pygame.font.Font(None, 100)
        self.font_medium = pygame.font.Font(None, 60)

        button_width = 260
        button_height = 60
        center_x = width // 2 - button_width // 2

        self.resume_button = Button(
            center_x, height // 2 - 80,
            button_width, button_height,
            "Resume", (0, 120, 0), (0, 170, 0)
        )

        self.settings_button = Button(
            center_x, height // 2 + 10,
            button_width, button_height,
            "Settings", (40, 80, 200), (70, 120, 255)
        )

        self.quit_button = Button(
            center_x, height // 2 + 100,
            button_width, button_height,
            "Main Menu", (120, 0, 0), (170, 0, 0)
        )

    def draw(self, screen):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title_surface = self.font_large.render("Paused", True, (255, 255, 255))
        screen.blit(title_surface, (self.width//2 - title_surface.get_width()//2, 150))

        mouse_pos = pygame.mouse.get_pos()

        self.resume_button.check_hover(mouse_pos)
        self.settings_button.check_hover(mouse_pos)
        self.quit_button.check_hover(mouse_pos)

        self.resume_button.draw(screen, self.font_medium)
        self.settings_button.draw(screen, self.font_medium)
        self.quit_button.draw(screen, self.font_medium)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if self.resume_button.is_clicked(mouse_pos, True):
                return "resume"
            if self.settings_button.is_clicked(mouse_pos, True):
                return "settings"
            if self.quit_button.is_clicked(mouse_pos, True):
                return "main_menu"

        return None


# ============================================================================
# SETTINGS MENU
# ============================================================================
class SettingsMenu:
    def __init__(self, width, height, volume_settings):
        """
        Settings menu with volume controls.

        Args:
            width, height: Screen dimensions
            volume_settings: VolumeSettings instance from main.py
        """
        self.width = width
        self.height = height
        self.volume_settings = volume_settings

        self.font_large = pygame.font.Font(None, 100)
        self.font_medium = pygame.font.Font(None, 60)
        self.font_small = pygame.font.Font(None, 40)

        # Slider dimensions
        slider_width = 400
        slider_height = 20
        center_x = width // 2 - slider_width // 2

        # Music volume slider (positioned higher)
        self.music_slider = Slider(
            center_x, height // 2 - 80,
            slider_width, slider_height,
            min_val=0.0, max_val=1.0,
            initial_val=volume_settings.music_volume
        )

        # SFX volume slider (positioned below music slider)
        self.sfx_slider = Slider(
            center_x, height // 2 + 40,
            slider_width, slider_height,
            min_val=0.0, max_val=1.0,
            initial_val=volume_settings.sfx_volume
        )

        # Back button (positioned at bottom)
        button_width = 260
        button_height = 60
        self.back_button = Button(
            width // 2 - button_width // 2, height // 2 + 180,
            button_width, button_height,
            "Back", (90, 90, 90), (140, 140, 140)
        )

    def draw(self, screen):
        """Draw settings menu with sliders."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (0, 0))

        # Title
        title = self.font_large.render("Settings", True, (255, 255, 255))
        screen.blit(title, (self.width//2 - title.get_width()//2, 150))

        # Draw sliders
        self.music_slider.draw(screen, self.font_small, "Music Volume")
        self.sfx_slider.draw(screen, self.font_small, "Sound Effects Volume")

        # Draw back button
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(screen, self.font_medium)

    def update(self, mouse_pos, mouse_pressed):
        """
        Update sliders and apply volume changes in real-time.
        Should be called every frame when settings menu is active.
        """
        # Update music slider
        if self.music_slider.update(mouse_pos, mouse_pressed):
            self.volume_settings.set_music_volume(self.music_slider.value)

        # Update SFX slider
        if self.sfx_slider.update(mouse_pos, mouse_pressed):
            self.volume_settings.set_sfx_volume(self.sfx_slider.value)

    def handle_events(self, event):
        """Handle button clicks."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button.is_clicked(mouse_pos, True):
                return "back"
        return None


# ============================================================================
# GAME OVER MENU
# ============================================================================
class GameOverMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font_large = pygame.font.Font(None, 120)
        self.font_medium = pygame.font.Font(None, 60)

        button_width = 260
        button_height = 60
        center_x = width // 2 - button_width // 2

        self.restart_button = Button(
            center_x, height // 2,
            button_width, button_height,
            "Restart", (0, 120, 0), (0, 170, 0)
        )

        self.main_menu_button = Button(
            center_x, height // 2 + 90,
            button_width, button_height,
            "Main Menu", (70, 70, 70), (120, 120, 120)
        )

    def draw(self, screen):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = self.font_large.render("Game Over", True, (255, 0, 0))
        screen.blit(title, (self.width//2 - title.get_width()//2, 150))

        mouse_pos = pygame.mouse.get_pos()

        self.restart_button.check_hover(mouse_pos)
        self.main_menu_button.check_hover(mouse_pos)

        self.restart_button.draw(screen, self.font_medium)
        self.main_menu_button.draw(screen, self.font_medium)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.restart_button.is_clicked(mouse_pos, True):
                return "restart"
            if self.main_menu_button.is_clicked(mouse_pos, True):
                return "main_menu"
        return None

class LevelSelectMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Fonts
        self.title_font = pygame.font.SysFont("bahnschrift", 64, bold=True)
        self.level_font = pygame.font.SysFont("bahnschrift", 36, bold=True)
        self.sub_font = pygame.font.SysFont("bahnschrift", 26)
        self.button_font = pygame.font.SysFont("bahnschrift", 30, bold=True)

        # Layout - 3 level cards
        card_w = 350
        card_h = 240
        gap = 60
        total_w = card_w * 3 + gap * 2
        start_x = (self.width - total_w) // 2
        y = self.height // 2 - card_h // 2 + 40

        self.level1_rect = pygame.Rect(start_x, y, card_w, card_h)
        self.level2_rect = pygame.Rect(start_x + card_w + gap, y, card_w, card_h)
        self.level3_rect = pygame.Rect(start_x + (card_w + gap) * 2, y, card_w, card_h)

        # Back button
        self.back_button = Button(
            self.width // 2 - 140,
            self.height - 140,
            280,
            70,
            "Back",
            (90, 90, 90),
            (130, 130, 130),
        )

        # Optional images
        self.ground_img = None
        self.cloud_img = None
        self.space_img = None  # Level 3 rymd (space) image

        base_dir = os.path.dirname(__file__)
        menu_dir = os.path.join(base_dir, "..", "assets", "menu")

        try:
            ground = os.path.join(menu_dir, "ground.png")
            cloud = os.path.join(menu_dir, "cloud.png")
            space = os.path.join(menu_dir, "rymd.png")  # Space theme for Level 3

            if os.path.exists(ground):
                self.ground_img = pygame.image.load(ground).convert_alpha()
            if os.path.exists(cloud):
                self.cloud_img = pygame.image.load(cloud).convert_alpha()
            if os.path.exists(space):
                self.space_img = pygame.image.load(space).convert_alpha()
        except Exception:
            self.ground_img = None
            self.cloud_img = None
            self.space_img = None

    # --------------------------------------------------

    def handle_events(self, event, level2_unlocked=True):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.back_button.is_clicked(mouse_pos, mouse_pressed):
            return "back"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.level1_rect.collidepoint(mouse_pos):
                return "start_level_1"

            if self.level2_rect.collidepoint(mouse_pos) and level2_unlocked:
                return "start_level_2"

            # Level 3 - alltid tillgänglig för testning
            if self.level3_rect.collidepoint(mouse_pos):
                return "start_level_3"

        return None

    # --------------------------------------------------

    def draw(self, screen, level2_unlocked=True):
        screen.fill((12, 12, 28))

        # Title
        title = self.title_font.render("SELECT LEVEL", True, (255, 255, 255))
        screen.blit(
            title,
            (self.width // 2 - title.get_width() // 2, 120),
        )

        self._draw_card(
            screen,
            self.level1_rect,
            self.ground_img,
            "Level 1",
            "Ground trip",
            locked=False,
        )

        self._draw_card(
            screen,
            self.level2_rect,
            self.cloud_img,
            "Level 2",
            "Cloud trip",
            locked=not level2_unlocked,
        )

        self._draw_card(
            screen,
            self.level3_rect,
            self.space_img,
            "Level 3",
            "Boss Fight",
            locked=False,  # Alltid upplåst för testning
        )

        self.back_button.draw(screen, self.button_font)

    # --------------------------------------------------

    def _draw_card(self, screen, rect, img, title, subtitle, locked=False):
        mouse_pos = pygame.mouse.get_pos()
        hovered = rect.collidepoint(mouse_pos) and not locked

        base_color = (35, 140, 90) if "Ground" in subtitle else (55, 95, 180)
        if title == "Level 3":
            base_color = (170, 40, 40)
        if locked:
            base_color = (70, 70, 80)

        # Shadow
        shadow = rect.copy()
        shadow.x += 8
        shadow.y += 10
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=18)

        # Card
        pygame.draw.rect(screen, base_color, rect, border_radius=18)
        pygame.draw.rect(
            screen,
            (255, 255, 255) if hovered else (0, 0, 0),
            rect,
            width=3,
            border_radius=18,
        )

        # Image area
        pad = 16
        img_rect = pygame.Rect(
            rect.x + pad,
            rect.y + pad,
            rect.w - pad * 2,
            rect.h - 110,
        )

        if img:
            scaled = pygame.transform.smoothscale(img, (img_rect.w, img_rect.h))
            screen.blit(scaled, img_rect)
        else:
            pygame.draw.rect(screen, (20, 20, 35), img_rect, border_radius=12)

        # Text
        t1 = self.level_font.render(title, True, (255, 255, 255))
        t2 = self.sub_font.render(subtitle, True, (220, 220, 220))

        screen.blit(
            t1,
            (rect.centerx - t1.get_width() // 2, rect.bottom - 82),
        )
        screen.blit(
            t2,
            (rect.centerx - t2.get_width() // 2, rect.bottom - 46),
        )

        if locked:
            overlay = pygame.Surface((rect.w, rect.h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 140))
            screen.blit(overlay, rect.topleft)

            lock_text = self.sub_font.render("LOCKED", True, (255, 255, 255))
            screen.blit(
                lock_text,
                (
                    rect.centerx - lock_text.get_width() // 2,
                    rect.centery - lock_text.get_height() // 2,
                ),
            )

# ============================================================================
# VICTORY MENU
# ============================================================================
class VictoryMenu:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font_large = pygame.font.Font(None, 120)
        self.font_medium = pygame.font.Font(None, 60)

        button_width = 260
        button_height = 60
        center_x = width // 2 - button_width // 2

        self.main_menu_button = Button(
            center_x, height // 2 + 120,
            button_width, button_height,
            "Main Menu", (0, 120, 0), (0, 170, 0)
        )

    def draw(self, screen, collected, total, level_score, total_score, time_seconds):

        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title = self.font_large.render("Victory!", True, (255, 255, 255))
        screen.blit(title, (self.width//2 - title.get_width()//2, 150))

        score = self.font_medium.render(f"{collected} / {total} Mushrooms", True, (255, 255, 255))
        screen.blit(score, (self.width//2 - score.get_width()//2, 320))
        
        time_text = self.font_medium.render(f"Time: {time_seconds}s", True, (255, 255, 255))
        screen.blit(time_text, (self.width//2 - time_text.get_width()//2, 390))

        level_text = self.font_medium.render(f"Level score: {level_score}", True, (255, 255, 255))
        screen.blit(level_text, (self.width//2 - level_text.get_width()//2, 450))

        total_text = self.font_medium.render(f"Total score: {total_score}", True, (255, 255, 255))
        screen.blit(total_text, (self.width//2 - total_text.get_width()//2, 510))

        mouse_pos = pygame.mouse.get_pos()
        self.main_menu_button.check_hover(mouse_pos)
        self.main_menu_button.draw(screen, self.font_medium)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if self.main_menu_button.is_clicked(mouse_pos, True):
                return "main_menu"
        return None

# ============================================================================
# SCORES MENU
# ============================================================================
class ScoresMenu:
    def __init__(self, width, height, background_path):
        self.width = width
        self.height = height

        self.background = pygame.image.load(background_path).convert()
        self.background = pygame.transform.scale(self.background, (width, height))

        self.title_font = pygame.font.SysFont("bahnschrift", 72, bold=True)
        self.header_font = pygame.font.SysFont("bahnschrift", 34, bold=True)
        self.row_font = pygame.font.SysFont("bahnschrift", 32)

        self.back_button = Button(
            self.width // 2 - 140,
            self.height - 140,
            280,
            70,
            "Back",
            (90, 90, 90),
            (130, 130, 130),
        )

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = pygame.mouse.get_pos()
            if self.back_button.is_clicked(mouse_pos, True):
                return "back"
        return None

    def draw(self, screen, particle_manager=None):
        # Bakgrund + partiklar (så det känns som ert spel)
        screen.blit(self.background, (0, 0))
        if particle_manager:
            particle_manager.update_and_draw(screen)

        # Mörk overlay för läsbarhet
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Title
        title = self.title_font.render("SCORES", True, (255, 245, 220))
        screen.blit(title, (self.width // 2 - title.get_width() // 2, 120))

        # Panel (”tabellen”)
        panel_w = 700
        panel_h = 420
        panel_x = self.width // 2 - panel_w // 2
        panel_y = 240
        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)

        # Shadow + panel
        shadow = panel_rect.copy()
        shadow.x += 10
        shadow.y += 12
        pygame.draw.rect(screen, (0, 0, 0), shadow, border_radius=18)

        pygame.draw.rect(screen, (20, 20, 30), panel_rect, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, width=2, border_radius=18)

        # Data
        last3 = get_last_scores(3)
        high = get_high_score()

        # Header row
        header_y = panel_y + 40
        col1_x = panel_x + 60
        col2_x = panel_x + panel_w - 160

        h1 = self.header_font.render("Latest runs", True, (255, 255, 255))
        h2 = self.header_font.render("Score", True, (255, 255, 255))
        screen.blit(h1, (col1_x, header_y))
        screen.blit(h2, (col2_x, header_y))

        # Divider
        pygame.draw.line(
            screen, (255, 255, 255),
            (panel_x + 40, header_y + 50),
            (panel_x + panel_w - 40, header_y + 50),
            2
        )

        # Rows
        row_y = header_y + 80
        labels = ["#1", "#2", "#3"]
        for i in range(3):
            label = labels[i]
            val = last3[i] if i < len(last3) else 0

            t_label = self.row_font.render(label, True, (220, 220, 220))
            t_val = self.row_font.render(str(val), True, (255, 255, 255))
            screen.blit(t_label, (col1_x, row_y + i * 60))
            screen.blit(t_val, (col2_x, row_y + i * 60))

        # High score box
        box_rect = pygame.Rect(panel_x + 40, panel_y + panel_h - 120, panel_w - 80, 80)
        pygame.draw.rect(screen, (55, 95, 180), box_rect, border_radius=14)
        pygame.draw.rect(screen, (0, 0, 0), box_rect, width=2, border_radius=14)

        hs_label = self.header_font.render("All-time record", True, (255, 255, 255))
        hs_val = self.header_font.render(str(high), True, (255, 255, 255))
        screen.blit(hs_label, (box_rect.x + 20, box_rect.y + 18))
        screen.blit(hs_val, (box_rect.right - hs_val.get_width() - 20, box_rect.y + 18))

        # Back button
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.check_hover(mouse_pos)
        self.back_button.draw(screen, pygame.font.SysFont("bahnschrift", 36, bold=True))

import os
import pygame
from player import Player


class BackgroundManager:
    """
    Hanterar bakgrundsbilder för en bana.
    - Laddar alla bilder i assets/maps/<level_name>/
    - Byter bild när spelaren når vänster/höger-kant
    """

    def __init__(self, width: int, height: int, level_name: str = "level1") -> None:
        self.width = width
        self.height = height
        self.level_name = level_name  # Store level name for index mapping

        base_dir = os.path.dirname(__file__)
        self.level_dir = os.path.join(base_dir, "..", "assets", "maps", level_name)

        image_files = [
            f
            for f in os.listdir(self.level_dir)
            if f.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
        image_files.sort()

        if not image_files:
            raise FileNotFoundError(f"Inga bakgrundsbilder hittades i {self.level_dir}")

        self.backgrounds: list[pygame.Surface] = []
        for name in image_files:
            path = os.path.join(self.level_dir, name)
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, (self.width, self.height))
            self.backgrounds.append(img)

        # Special handling for level2: duplicate backgrounds to cover 5 screens
        # Level 2 has 3 images but needs 5 screens (screens 3-7)
        # Pattern: [trippycloud1.png, trippycloud2.png, trippycloud3.png] -> [img0, img1, img2, img1, img2]
        if level_name == "level2" and len(self.backgrounds) == 3:
            # Duplicate backgrounds: [0, 1, 2] -> [0, 1, 2, 1, 2]
            self.backgrounds.append(self.backgrounds[1])  # Add trippycloud2.png again
            self.backgrounds.append(self.backgrounds[2])  # Add trippycloud3.png again

        self.current_index = 0

    def update_for_player(self, player: Player, boss_active: bool = False) -> None:
        """Uppdatera vilken bakgrund som ska visas baserat på spelarens position."""
        # Calculate min/max screen indices based on level
        if self.level_name == "level2":
            min_index = 3  # Level 2 starts at screen 3
            max_index = 7  # Level 2 ends at screen 7
        elif self.level_name == "level3":
            min_index = 8  # Level 3 starts at screen 8
            max_index = 10  # Level 3 ends at screen 10
        else:
            min_index = 0
            max_index = len(self.backgrounds) - 1

        # Om boss är aktiv på screen 9, tillåt inte övergångar
        if boss_active and self.current_index == 9:
            # Clampa spelaren till skärmgränser
            if player.x <= 0:
                player.x = 0
            elif player.x + player.width >= self.width:
                player.x = self.width - player.width
            return  # Processar inte screen transitions

        # gå höger: byt bild tills vi nått sista
        if player.x + player.width >= self.width:
            if self.current_index < max_index:
                self.current_index += 1
                player.x = 50
            else:
                player.x = self.width - player.width  # stanna på sista

        # gå vänster: byt bild tills vi nått första
        elif player.x <= 0:
            if self.current_index > min_index:
                self.current_index -= 1
                player.x = self.width - player.width - 50
            else:
                player.x = 0  # stanna på första

    def draw(self, screen: pygame.Surface) -> None:
        """Rita aktuell bakgrund."""
        # Map screen index to background array index
        # Level 2: screens 3-7 map to backgrounds 0-4
        # Level 3: screens 8-10 map to backgrounds 0-2
        # Level 1: screens 0-2 map to backgrounds 0-2
        if self.level_name == "level2":
            bg_index = self.current_index - 3  # Map 3->0, 4->1, 5->2, 6->3, 7->4
        elif self.level_name == "level3":
            bg_index = self.current_index - 8  # Map 8->0, 9->1, 10->2
        else:
            bg_index = self.current_index

        screen.blit(self.backgrounds[bg_index], (0, 0))

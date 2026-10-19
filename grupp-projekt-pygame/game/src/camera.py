import pygame

class Camera:
    """
    Kamerasystem för boss-arena zoom-effekt.
    Skalar ner allt som ritas för att få boss att se större ut.
    Fullscreen 1920x1080 men allt renderas i mindre skala.
    """
    def __init__(self, screen_width, screen_height, zoom_level=1.0):
        """
        Initialisera kamera med zoom-nivå.

        Args:
            screen_width: Skärmens bredd (1920)
            screen_height: Skärmens höjd (1080)
            zoom_level: Zoom-nivå (0.5 = 50% zoom out, allt blir hälften så stort)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom_level = zoom_level

        # Beräkna offset för att centrera den zoomade vyn
        self.offset_x = int(screen_width * (1 - zoom_level) / 2)
        self.offset_y = int(screen_height * (1 - zoom_level) / 2)

    def transform_pos(self, x, y):
        """
        Transformera en position med zoom och offset.

        Args:
            x: Original X-position
            y: Original Y-position

        Returns:
            (new_x, new_y): Transformerad position
        """
        new_x = int(x * self.zoom_level + self.offset_x)
        new_y = int(y * self.zoom_level + self.offset_y)
        return (new_x, new_y)

    def transform_size(self, width, height):
        """
        Transformera en storlek med zoom.

        Args:
            width: Original bredd
            height: Original höjd

        Returns:
            (new_width, new_height): Transformerad storlek
        """
        new_width = int(width * self.zoom_level)
        new_height = int(height * self.zoom_level)
        return (new_width, new_height)

    def transform_rect(self, rect):
        """
        Transformera en pygame.Rect med zoom och offset.

        Args:
            rect: Original pygame.Rect

        Returns:
            pygame.Rect: Transformerad rect
        """
        new_x, new_y = self.transform_pos(rect.x, rect.y)
        new_width, new_height = self.transform_size(rect.width, rect.height)
        return pygame.Rect(new_x, new_y, new_width, new_height)

    def transform_surface(self, surface):
        """
        Skala en surface enligt zoom-nivån.

        Args:
            surface: Original surface

        Returns:
            pygame.Surface: Skalad surface
        """
        width, height = surface.get_size()
        new_width, new_height = self.transform_size(width, height)

        if new_width > 0 and new_height > 0:
            return pygame.transform.scale(surface, (new_width, new_height))
        return surface

    def is_zoomed(self):
        """
        Kolla om kameran har zoom.
        Returns: True om zoom är aktiv
        """
        return self.zoom_level != 1.0

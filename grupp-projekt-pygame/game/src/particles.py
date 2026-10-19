import pygame
import random


class Particle:
    def __init__(self, x, y, color, screen_height):
        self.x = x
        self.y = y
        self.color = color
        self.screen_height = screen_height

        # Startstorlek
        self.start_size = random.randint(4, 8)
        self.size = self.start_size

        # Lugn fart uppåt
        self.speed_y = random.uniform(-1.2, -2.4)
        self.speed_x = random.uniform(-0.4, 0.4)

        # Transparens
        self.alpha = 255

        # Bas-fade
        self.base_fade = random.uniform(0.2, 0.35)

    def update(self):
        # Rörelse
        self.x += self.speed_x
        self.y += self.speed_y

        # Höjd-baserad fade: ju högre upp → snabbare fade
        height_factor = max(0, (self.screen_height - self.y) / self.screen_height)
        fade_amount = self.base_fade + (height_factor * 0.8)
        self.alpha -= fade_amount

        # Storlek minskar med höjden
        self.size = max(1, int(self.start_size * (1 - height_factor * 0.9)))

        # Död om osynlig eller utanför toppen
        return self.alpha > 0 and self.y > -20

    def draw(self, screen):
        if self.alpha <= 0 or self.size <= 0:
            return

        surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(
            surface,
            (*self.color, int(self.alpha)),
            (self.size, self.size),
            self.size
        )
        screen.blit(surface, (self.x, self.y))


class ParticleManager:
    def __init__(self, width, height, max_particles=200):
        self.width = width
        self.height = height
        self.particles = []
        self.max_particles = max_particles

    def spawn(self):
        x = random.randint(0, self.width)
        y = self.height + 5

        color = random.choice([
            (255, 80, 100),
            (120, 200, 255),
            (255, 180, 70),
            (160, 120, 255),
        ])

        if len(self.particles) < self.max_particles:
            self.particles.append(Particle(x, y, color, self.height))

    def update_and_draw(self, screen):
        # FÄRRE PRICKAR: ganska låg spawn rate
        if random.random() < 0.2:
            self.spawn()
        if random.random() < 0.05:
            self.spawn()

        for p in self.particles[:]:
            if p.update():
                p.draw(screen)
            else:
                self.particles.remove(p)

import pygame
import sys

# Initiera pygame
pygame.init()

# Skapa en ruta (bredd x höjd)
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Mitt första Pygame-fönster")

# Välj en färg (RGB: röd, grön, blå)
bakgrundsfärg = (50, 150, 200)

# Spelloopen (körs tills man stänger fönstret)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fyll rutan med bakgrundsfärg
    screen.fill(bakgrundsfärg)

    # Uppdatera skärmen
    pygame.display.flip()

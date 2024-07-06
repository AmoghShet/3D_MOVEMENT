import pygame
import math
from pygame.math import Vector3

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Wireframe")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Player variables
pos = Vector3(0, 0, 0)
angle = 0

# Camera variables
FOV = 90
draw_distance = 1000

# Create a simple "world" (just a grid for now)
grid_size = 10
grid = []
for x in range(-grid_size, grid_size + 1):
    for z in range(-grid_size, grid_size + 1):
        grid.append(Vector3(x * 100, 0, z * 100))

def rotate2d(pos, rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)
    return x * c - y * s, y * c + x * s

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle input
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle -= 0.03
    if keys[pygame.K_RIGHT]:
        angle += 0.03
    if keys[pygame.K_UP]:
        pos.x += math.sin(angle) * 2
        pos.z += math.cos(angle) * 2
    if keys[pygame.K_DOWN]:
        pos.x -= math.sin(angle) * 2
        pos.z -= math.cos(angle) * 2

    # Clear the screen
    display.fill((0, 0, 0))

    # Draw the grid
    for point in grid:
        x, y, z = point - pos
        x, z = rotate2d((x, z), angle)
        f = FOV / max(z, 0.1)
        x, y = x * f, y * f
        pygame.draw.circle(display, WHITE, (int(x) + width // 2, int(y) + height // 2), 2)

    # Update the display
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

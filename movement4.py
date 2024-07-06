import pygame
import math
from pygame.math import Vector3

# Initialize pygame
pygame.init()

# Set up display dimensions and create display window
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Wireframe")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize player position, angle, and jumping state
pos = Vector3(0, 0, 0)
angle = 0
vertical_speed = 0
is_jumping = False

# Set up field of view and draw distance for the 3D perspective
FOV = 90
draw_distance = 1000

# Define grid size and create grid points
grid_size = 10
grid = []
for x in range(-grid_size, grid_size + 1):
    for z in range(-grid_size, grid_size + 1):
        grid.append(Vector3(x * 100, 0, z * 100))

# Function to rotate a point around the Z-axis
def rotate2d(pos, rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)
    return x * c - y * s, y * c + x * s

# Set up clock for managing frame rate
clock = pygame.time.Clock()
running = True

# Define movement speeds
normal_speed = 200
sprint_speed = 400

# Main game loop
while running:
    # Calculate delta time in seconds
    dt = clock.tick(60) / 1000

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                vertical_speed = 300  # Initial jump velocity
                is_jumping = True

    # Handle key presses for movement and rotation
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle -= 2 * dt
    if keys[pygame.K_RIGHT]:
        angle += 2 * dt

    # Determine movement speed based on sprint key (left Shift)
    movement_speed = sprint_speed if keys[pygame.K_LSHIFT] else normal_speed

    if keys[pygame.K_UP]:
        pos.x += math.sin(angle) * movement_speed * dt
        pos.z += math.cos(angle) * movement_speed * dt
    if keys[pygame.K_DOWN]:
        pos.x -= math.sin(angle) * movement_speed * dt
        pos.z -= math.cos(angle) * movement_speed * dt

    # Apply gravity and update vertical position
    vertical_speed -= 600 * dt  # Gravity
    pos.y += vertical_speed * dt

    # Handle ground collision
    if pos.y < 0:
        pos.y = 0
        vertical_speed = 0
        is_jumping = False

    # Clear display with black background
    display.fill((0, 0, 0))

    # Draw the grid
    for point in grid:
        x, y, z = point - pos  # Translate point relative to player position
        x, z = rotate2d((x, z), angle)  # Rotate point around player

        if z > 0:  # Only draw points in front of the player
            f = FOV / z  # Perspective projection factor
            x, y = x * f, y * f
            
            # Convert 3D coordinates to 2D screen coordinates
            screen_x = int(x) + width // 2
            screen_y = height // 2 - int(y)
            
            # Calculate top and bottom y-coordinates for vertical lines
            top_y = screen_y - int(100 * f)
            bottom_y = screen_y + int(100 * f)
            
            # Draw vertical lines representing the grid
            pygame.draw.line(display, WHITE, (screen_x, top_y), (screen_x, bottom_y), 1)

    # Update the display
    pygame.display.flip()

# Quit pygame
pygame.quit()
import pygame
import math
from pygame.math import Vector3

# Initialize Pygame
pygame.init()

# Set up display dimensions and create display window
width, height = 800, 600
display = pygame.display.set_mode((width, height))
pygame.display.set_caption("3D Wireframe")

# Define colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize position and angle for the camera
pos = Vector3(0, 0, 0)
angle = 0

# Set field of view (FOV) and draw distance
FOV = 90
draw_distance = 1000

# Create a grid of points
grid_size = 10
grid = []
for x in range(-grid_size, grid_size + 1):
    for z in range(-grid_size, grid_size + 1):
        grid.append(Vector3(x * 100, 0, z * 100))

# Define a function to rotate 2D points
def rotate2d(pos, rad):
    x, y = pos
    s, c = math.sin(rad), math.cos(rad)
    return x * c - y * s, y * c + x * s

# Initialize clock and running flag
clock = pygame.time.Clock()
running = True

# Main loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle key presses for camera movement and rotation
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle -= 0.03  # Rotate left
    if keys[pygame.K_RIGHT]:
        angle += 0.03  # Rotate right
    if keys[pygame.K_UP]:
        pos.x += math.sin(angle) * 2  # Move forward
        pos.z += math.cos(angle) * 2
    if keys[pygame.K_DOWN]:
        pos.x -= math.sin(angle) * 2  # Move backward
        pos.z -= math.cos(angle) * 2

    # Clear the display
    display.fill((0, 0, 0))

    # Render the grid
    for point in grid:
        x, y, z = point - pos  # Translate point relative to camera position
        x, z = rotate2d((x, z), angle)  # Rotate point around the Y axis
        
        if z > 0:  # Only render points in front of the camera
            f = FOV / z  # Perspective projection scaling factor
            x, y = x * f, y * f  # Apply perspective projection
            
            # Calculate top and bottom points of the vertical line
            top_y = y - 100 * f  # 100 is the height of the line
            bottom_y = y + 100 * f
            
            # Convert to screen coordinates
            screen_x = int(x) + width // 2
            screen_top_y = int(top_y) + height // 2
            screen_bottom_y = int(bottom_y) + height // 2
            
            # Draw the vertical line
            pygame.draw.line(display, WHITE, (screen_x, screen_top_y), (screen_x, screen_bottom_y), 1)

    # Update the display
    pygame.display.flip()
    # Cap the frame rate to 60 FPS
    clock.tick(60)

# Quit Pygame
pygame.quit()

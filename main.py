import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width = 1000
height = 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("NISHATTACK")

# Load the player image and scale it
player_image_original = pygame.image.load("nishtha.png")
player_image_original = pygame.transform.scale(player_image_original, (100, 100))  # Scale to desired size
player_rect = player_image_original.get_rect()
player_rect.center = (width // 2, height // 2)
player_speed = 1

# Load enemy images and scale them
enemy_images = []
enemy_instances = []  # List to hold instances of enemy images
for i in range(5):
    enemy_image = pygame.image.load(f"enemy{i + 1}.png")
    # Calculate width and height while maintaining the aspect ratio
    aspect_ratio = enemy_image.get_width() / enemy_image.get_height()
    new_width = 75  # Adjust the desired width
    new_height = int(new_width / aspect_ratio)
    enemy_image = pygame.transform.scale(enemy_image, (new_width, new_height))
    enemy_images.append(enemy_image)
    # Generate multiple instances of each enemy with initial positions only at the edges
    for _ in range(1):  # Adjust the number of instances as needed
        random_side = random.choice(["left", "right", "top"])  # Restrict to top, left, or right
        if random_side == "left":
            initial_x = 0 - new_width
            initial_y = random.randint(0, height - new_height)
        elif random_side == "right":
            initial_x = width
            initial_y = random.randint(0, height - new_height)
        else:  # top
            initial_x = random.randint(0, width - new_width)
            initial_y = 0 - new_height
        enemy_rect = pygame.Rect(initial_x, initial_y, new_width, new_height)
        direction = random.choice(["left", "right", "down"])  # Adjusted directions
        if random_side == "left":
            direction = "right"
        elif random_side == "right":
            direction = "left"
        enemy_instances.append((enemy_image, enemy_rect, direction))

# Define enemy speed
enemy_speed = 1

# Variable to track if player image is flipped
player_flipped = False

# Game over screen function
def game_over_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Restart the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Quit the game
        window.fill((0, 0, 0))  # Black background
        # Display game over text
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        window.blit(game_over_text, ((width - game_over_text.get_width()) // 2, (height - game_over_text.get_height()) // 2))
        # Display instructions
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Press Enter to play again or Escape to quit", True, (255, 255, 255))
        window.blit(instruction_text, ((width - instruction_text.get_width()) // 2, (height + game_over_text.get_height()) // 2 + 20))
        pygame.display.flip()

# Reset game state function
def reset_game_state():
    global player_rect, enemy_instances
    player_rect.center = (width // 2, height // 2)
    enemy_instances = []
    for i in range(5):
        for _ in range(1):
            random_side = random.choice(["left", "right", "top"])
            if random_side == "left":
                initial_x = 0 - new_width
                initial_y = random.randint(0, height - new_height)
            elif random_side == "right":
                initial_x = width
                initial_y = random.randint(0, height - new_height)
            else:  # top
                initial_x = random.randint(0, width - new_width)
                initial_y = 0 - new_height
            enemy_rect = pygame.Rect(initial_x, initial_y, new_width, new_height)
            direction = random.choice(["left", "right", "down"])
            if random_side == "left":
                direction = "right"
            elif random_side == "right":
                direction = "left"
            enemy_instances.append((enemy_images[i], enemy_rect, direction))

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Handle player movement and flipping
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        if player_flipped:
            player_image_original = pygame.transform.flip(player_image_original, True, False)  # Flip back to original
            player_flipped = False
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        if not player_flipped:
            player_image_original = pygame.transform.flip(player_image_original, True, False)  # Flip horizontally
            player_flipped = True
        player_rect.x += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed
    
    # Ensure the player stays within the screen boundaries
    player_rect.x = max(0, min(player_rect.x, width - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, height - player_rect.height))
    
    # Move enemies in their fixed directions
    for enemy_image, enemy_rect, direction in enemy_instances:
        if direction == "left":
            enemy_rect.x -= enemy_speed
        elif direction == "right":
            enemy_rect.x += enemy_speed
        elif direction == "up":
            enemy_rect.y -= enemy_speed
        elif direction == "down":
            enemy_rect.y += enemy_speed
        
        # Remove enemies that go off-screen
        if not window.get_rect().colliderect(enemy_rect):
            enemy_instances.remove((enemy_image, enemy_rect, direction))
            # Re-add enemy with initial position at the edge and fixed direction if it goes off-screen
            random_side = random.choice(["left", "right", "top"])
            if random_side == "left":
                enemy_rect.topleft = (0 - enemy_rect.width, random.randint(0, height - enemy_rect.height))
                enemy_instances.append((enemy_image, enemy_rect, "right"))
            elif random_side == "right":
                enemy_rect.topleft = (width, random.randint(0, height - enemy_rect.height))
                enemy_instances.append((enemy_image, enemy_rect, "left"))
            else:  # top
                enemy_rect.topleft = (random.randint(0, width - enemy_rect.width), 0 - enemy_rect.height)
                enemy_instances.append((enemy_image, enemy_rect, "down"))
    
    # Check for collisions between player and enemies
    for enemy_image, enemy_rect, _ in enemy_instances:
        if player_rect.colliderect(enemy_rect):
            game_over_screen()  # Display game over screen if collision occurs
            reset_game_state()  # Reset game state after game over
    
    # Render objects
    window.fill((255, 255, 255))  # White background
    window.blit(player_image_original, player_rect)  # Draw the player onto the window
    for enemy_image, enemy_rect, _ in enemy_instances:
        window.blit(enemy_image, enemy_rect)  # Draw enemies onto the window
    pygame.display.flip()  # Update the display

# Clean up
pygame.quit()
sys.exit()

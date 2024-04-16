import pygame
import sys
import random
import time

# Initialize Pygame
pygame.init()

# Set up the game window
width = 1600
height = 900
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("NISHATTACK")

# Load the player image and scale it
player_image_original = pygame.image.load("imgs/nishtha.png")
aspect_ratio = player_image_original.get_width() / player_image_original.get_height()
img_width = 70
player_image_original = pygame.transform.scale(player_image_original, (img_width, int(img_width / aspect_ratio)))  # Scale to desired size
player_rect = player_image_original.get_rect()
player_rect.center = (width // 2, height // 2)
player_speed = 1

# Load enemy images and scale them
enemy_images = []
enemy_instances = []  # List to hold instances of enemy images
for i in range(5):
    enemy_image = pygame.image.load(f"imgs/enemy{i + 1}.png")
    # Calculate width and height while maintaining the aspect ratio
    aspect_ratio = enemy_image.get_width() / enemy_image.get_height()
    new_width = 75  # Adjust the desired width
    if (i==2):
        new_width = 200
    elif(i==3):
        new_width = 100
    elif (i==4):
        new_width = 150
    new_height = int(new_width / aspect_ratio)
    enemy_image = pygame.transform.scale(enemy_image, (new_width, new_height))
    enemy_images.append(enemy_image)
    # Generate multiple instances of each enemy with initial positions only at the edges
    for _ in range(2):  # Adjust the number of instances as needed
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

# Set start time
start_time = time.time()

# Game over screen function
def game_over_screen(enemy_image, elapsed_time):
    # Load the Nishtha image and scale it
    end_image = pygame.image.load("imgs/nishtha.png")
    aspect_ratio = end_image.get_width() / end_image.get_height()
    img_width = 150
    end_image = pygame.transform.scale(end_image, (img_width, int(img_width / aspect_ratio)))  # Scale to desired size

    # Display collision image
    ew_image = enemy_image
    aspect_ratio = ew_image.get_width() / ew_image.get_height()
    new_width = 200
    new_height = int(new_width / aspect_ratio)
    ew_image = pygame.transform.scale(ew_image, (new_width, new_height))

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
        # Display Nishtha and enemy_image that she collided with
        window.blit(end_image, ((width - end_image.get_width()) // 2, (height - end_image.get_height()) // 2 - 100))
        window.blit(ew_image, ((width - ew_image.get_width()) // 2 - 300, (height - ew_image.get_height()) // 2 - 100))
        # Display game over text
        font = pygame.font.Font(None, 64)
        game_over_text = font.render("EWWWW!!", True, (255, 0, 0))
        window.blit(game_over_text, ((width - game_over_text.get_width()) // 2, (height - game_over_text.get_height()) // 2))
        # Display score and instructions
        score_font = pygame.font.Font(None, 32)
        score_text = font.render("SCORE: {:.0f}".format(elapsed_time), True, (255, 255, 255))
        window.blit(score_text, ((width - score_text.get_width()) // 2, (height + game_over_text.get_height()) // 2 + 20))

        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Press Enter to play again or Escape to quit", True, (255, 255, 255))
        window.blit(instruction_text, ((width - instruction_text.get_width()) // 2, (height + game_over_text.get_height()) // 2 + 100))
        pygame.display.flip()

# Reset game state function
def reset_game_state():
    global player_rect, enemy_instances
    player_rect.center = (width // 2, height // 2)
    enemy_instances = []
    for i in range(5):
        for _ in range(2):
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

# Start screen function
def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True  # Start the game
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()  # Quit the game
        window.fill((0, 0, 0))  # Black background
        # Display game title
        font = pygame.font.Font(None, 100)
        title_text = font.render("NISHATTACK", True, (255, 255, 255))
        window.blit(title_text, ((width - title_text.get_width()) // 2, (height - title_text.get_height()) // 2 - 100))
        # Display instructions
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render("Press Enter to play", True, (255, 255, 255))
        window.blit(instruction_text, ((width - instruction_text.get_width()) // 2, (height + title_text.get_height()) // 2 + 20))
        pygame.display.flip()

# Main game loop
start_screen()  # Show the start screen before starting the game
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
            game_over_screen(enemy_image, elapsed_time)  # Display game over screen if collision occurs
            reset_game_state()  # Reset game state after game over
            start_time = time.time()
    
    # Render objects
    window.fill((255, 255, 255))  # White background
    window.blit(player_image_original, player_rect)  # Draw the player onto the window
    for enemy_image, enemy_rect, _ in enemy_instances:
        window.blit(enemy_image, enemy_rect)  # Draw enemies onto the window

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # RENDER THE TEXT
    font = pygame.font.Font(None, 70)
    # Render the text with red background
    text_surface = font.render("TIME: {:.0f}".format(elapsed_time), True, (0, 0, 0))
    text_rect = text_surface.get_rect()
    text_rect.topleft = (20, 20)

    # Create a surface for the red background with a border
    border_width = 4  # Adjust border width as needed
    background_width = text_rect.width + 2 * border_width
    background_height = text_rect.height + 2 * border_width
    background_surface = pygame.Surface((background_width, background_height))
    background_surface.fill((0, 0, 0))  # Black border color
    inner_surface = pygame.Surface((text_rect.width, text_rect.height))
    inner_surface.fill((255, 255, 0))  # Red background color
    background_surface.blit(inner_surface, (border_width, border_width))

    # Blit the red background onto the main window
    window.blit(background_surface, text_rect)

    # Blit the text onto the red background
    window.blit(text_surface, (text_rect.left + border_width, text_rect.top + border_width))



    pygame.display.flip()  # Update the display

# Clean up
pygame.quit()
sys.exit()

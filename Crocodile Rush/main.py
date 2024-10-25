import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 450
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Crocodile Swim")

# Colors
WATER_COLOR = (135, 206, 250)  # Light blue for water
LOG_COLOR = (139, 69, 19)      # Brown for logs
BUBBLE_COLOR = (255, 255, 255)  # White for bubbles

# Load crocodile image (replace 'crocodile.png' with your image file)
croc_image = pygame.image.load('crocodile.png')
croc_image = pygame.transform.scale(croc_image, (200, 50))  # Update to the new dimensions
croc_x, croc_y = 100, SCREEN_HEIGHT // 2  # Starting position

# Crocodile settings
croc_speed = 5
is_diving = False
dive_timer = 0
MAX_DIVE_TIME = 6000  # in milliseconds (6 seconds)

# Log settings
log_width = random.randint(150, 300)  # Random initial width of the log
log_height = 20
log_x = SCREEN_WIDTH
log_y = SCREEN_HEIGHT // 2 - log_height // 2  # Floating above the crocodile
log_speed = 5

# Score settings
score = 0
high_score = 0
font = pygame.font.Font(None, 36)  # Default font and size

# Bubble settings
bubbles = [{"x": random.randint(0, SCREEN_WIDTH), "y": SCREEN_HEIGHT, "speed": random.uniform(1, 3)} for _ in range(10)]

# Fish settings
fish_image = pygame.image.load('fish.png')
fish_image = pygame.transform.scale(fish_image, (30, 15))  # Scale to fit the environment
fish_swimming = [{"x": random.randint(0, SCREEN_WIDTH), "y": random.randint(50, SCREEN_HEIGHT - 50), "speed": random.uniform(1, 2)} for _ in range(5)]

# Clock
clock = pygame.time.Clock()

# Game loop
running = True
warning_displayed = False  # Variable to track if the warning has been shown
while running:
    screen.fill(WATER_COLOR)  # Draw water

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key press handling
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        if dive_timer < MAX_DIVE_TIME:
            is_diving = True
            dive_timer += clock.get_time()  # Increment dive timer
            croc_y = SCREEN_HEIGHT // 2 + 50  # Crocodile dives down
            
            # Check for warning
            if dive_timer >= 5000 and not warning_displayed:
                warning_displayed = True  # Set warning flag
                print("Crocodile is unable to dive for more than 5 seconds")  # Display warning message

            # Check for game over condition (after warning)
            if dive_timer >= MAX_DIVE_TIME:
                print("Game Over! Crocodile held dive too long!")
                if score > high_score:
                    high_score = score  # Update high score if current score is higher
                score = 0  # Reset score after collision
                log_x = SCREEN_WIDTH  # Reset log position
                log_speed = 5  # Reset speed after collision
                dive_timer = 0  # Reset dive timer
                warning_displayed = False  # Reset warning for next game
                is_diving = False  # Ensure diving is reset
        else:
            # Automatically float if the timer exceeds maximum dive time
            is_diving = False
    else:
        is_diving = False
        dive_timer = 0  # Reset dive timer when the space key is released
        warning_displayed = False  # Reset warning when space is released
        croc_y = SCREEN_HEIGHT // 2  # Crocodile returns to the surface

    # Move log
    log_x -= log_speed
    if log_x < -log_width:
        log_x = SCREEN_WIDTH + random.randint(100, 300)  # Randomize the distance between logs
        log_width = random.randint(60, 120)              # Randomize the log length
        log_speed += 0.2                                 # Gradually increase speed as logs respawn
        score += 1                                       # Increase score each time a log is avoided

    # Move bubbles
    for bubble in bubbles:
        bubble["y"] -= bubble["speed"]
        if bubble["y"] < 0:  # Reset bubble to bottom when it reaches the top
            bubble["x"] = random.randint(0, SCREEN_WIDTH)
            bubble["y"] = SCREEN_HEIGHT
            bubble["speed"] = random.uniform(1, 3)
        pygame.draw.circle(screen, BUBBLE_COLOR, (int(bubble["x"]), int(bubble["y"])), 5)

    # Move fish
    for fish in fish_swimming:
        fish["x"] -= fish["speed"]
        if fish["x"] < -30:  # Reset fish to the right when it swims off the left side
            fish["x"] = SCREEN_WIDTH + random.randint(10, 100)
            fish["y"] = random.randint(50, SCREEN_HEIGHT - 50)
            fish["speed"] = random.uniform(1, 2)
        screen.blit(fish_image, (fish["x"], fish["y"]))

    # Draw crocodile
    screen.blit(croc_image, (croc_x, croc_y))

    # Draw log
    pygame.draw.rect(screen, LOG_COLOR, (log_x, log_y, log_width, log_height))

    # Check for collision
    croc_rect = croc_image.get_rect(topleft=(croc_x, croc_y))
    log_rect = pygame.Rect(log_x, log_y, log_width, log_height)
    if croc_rect.colliderect(log_rect) and not is_diving:
        print("Game Over!")
        if score > high_score:
            high_score = score  # Update high score if current score is higher
        score = 0              # Reset score after collision
        log_x = SCREEN_WIDTH    # Reset log position to start again
        log_speed = 5           # Reset speed after collision

    # Display scores
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    high_score_text = font.render(f"High Score: {high_score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (10, 40))

    # Update display and tick the clock
    pygame.display.flip()
    clock.tick(30)  # Frame rate (30 FPS)

# Quit the game
pygame.quit()
sys.exit()

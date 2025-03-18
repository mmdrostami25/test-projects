import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Snake and apple size
BLOCK_SIZE = 20

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def message(msg, color, y_displace=0, size=50):
    font_style = pygame.font.SysFont(None, size)
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH/6, HEIGHT/2 + y_displace])

def game_loop():
    game_over = False
    game_close = False

    # Initial position and speed
    x = WIDTH / 2
    y = HEIGHT / 2
    dx = 0
    dy = 0

    snake_list = []
    snake_length = 1

    # Generate first apple
    apple_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    apple_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("Game Over! Press Q-Quit or C-Play Again", RED)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and dx != BLOCK_SIZE:
                    dx = -BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_RIGHT and dx != -BLOCK_SIZE:
                    dx = BLOCK_SIZE
                    dy = 0
                elif event.key == pygame.K_UP and dy != BLOCK_SIZE:
                    dy = -BLOCK_SIZE
                    dx = 0
                elif event.key == pygame.K_DOWN and dy != -BLOCK_SIZE:
                    dy = BLOCK_SIZE
                    dx = 0

        # Check boundaries collision
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        x += dx
        y += dy
        screen.fill(BLACK)
        
        # Draw apple
        pygame.draw.rect(screen, RED, [apple_x, apple_y, BLOCK_SIZE, BLOCK_SIZE])
        
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)
        
        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check self collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        pygame.display.update()

        # Eat apple
        if x == apple_x and y == apple_y:
            apple_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            apple_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        clock.tick(10)

    pygame.quit()
    quit()

game_loop()
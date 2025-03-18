import pygame
import random

pygame.init()

# تنظیمات
WIDTH = 600
HEIGHT = 400
CELL_SIZE = 20
SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# رنگ‌ها
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# جهت‌ها
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.body = [(WIDTH//2, HEIGHT//2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.grow = False

    def move(self):
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0] * CELL_SIZE) % WIDTH,
            (head[1] + self.direction[1] * CELL_SIZE) % HEIGHT
        )
        self.body.insert(0, new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def check_collision(self):
        return len(self.body) != len(set(self.body))

class Food:
    def __init__(self):
        self.position = self.random_position()

    def random_position(self):
        return (
            random.randrange(0, WIDTH, CELL_SIZE),
            random.randrange(0, HEIGHT, CELL_SIZE)
        )

snake = Snake()
food = Food()
score = 0
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != DOWN:
                snake.direction = UP
            elif event.key == pygame.K_DOWN and snake.direction != UP:
                snake.direction = DOWN
            elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                snake.direction = LEFT
            elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                snake.direction = RIGHT

    snake.move()

    # خوردن غذا
    if snake.body[0] == food.position:
        snake.grow = True
        food.position = food.random_position()
        score += 10
        
        SPEED += 0.5
        
    # برخورد با بدن
    if snake.check_collision():
        running = False

    # رسم اجزا
    screen.fill(BLACK)
    
    for segment in snake.body:
        pygame.draw.rect(screen, GREEN, 
                        (segment[0], segment[1], CELL_SIZE, CELL_SIZE))
    
    pygame.draw.rect(screen, RED, 
                   (food.position[0], food.position[1], CELL_SIZE, CELL_SIZE))
    
    text = font.render(f"Score: {score}", True, GREEN)
    screen.blit(text, (10, 10))
    
    pygame.display.flip()
    clock.tick(SPEED)

pygame.quit()
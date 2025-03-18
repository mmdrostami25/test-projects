import pygame
import random

pygame.init()

# تنظیمات پنجره
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# رنگ‌ها
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# اندازه راکت‌ها
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 90
BALL_SIZE = 20

# سرعت اولیه
paddle_speed = 5
ball_speed_x = 4 * random.choice([1, -1])
ball_speed_y = 4 * random.choice([1, -1])

# موقعیت اولیه
player1 = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
player2 = pygame.Rect(WIDTH - 45, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

# امتیاز
score1 = 0
score2 = 0
font = pygame.font.Font(None, 74)

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # کنترل راکت‌ها
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player1.top > 0:
        player1.y -= paddle_speed
    if keys[pygame.K_s] and player1.bottom < HEIGHT:
        player1.y += paddle_speed
    if keys[pygame.K_UP] and player2.top > 0:
        player2.y -= paddle_speed
    if keys[pygame.K_DOWN] and player2.bottom < HEIGHT:
        player2.y += paddle_speed

    # حرکت توپ
    ball.x += ball_speed_x
    ball.y += ball_speed_y

    # برخورد با دیوارها
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        
    # برخورد با راکت‌ها
    if ball.colliderect(player1) or ball.colliderect(player2):
        ball_speed_x *= -1
        ball_speed_y *= random.uniform(0.8, 1.2)

    # امتیازدهی
    if ball.left <= 0:
        score2 += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= random.choice([1, -1])
        
    if ball.right >= WIDTH:
        score1 += 1
        ball.center = (WIDTH//2, HEIGHT//2)
        ball_speed_x *= random.choice([1, -1])

    # رسم اجزا
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player1)
    pygame.draw.rect(screen, WHITE, player2)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    
    # نمایش امتیاز
    text = font.render(str(score1), True, WHITE)
    screen.blit(text, (WIDTH//4, 20))
    text = font.render(str(score2), True, WHITE)
    screen.blit(text, (3*WIDTH//4, 20))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
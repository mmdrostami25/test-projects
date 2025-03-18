import pygame

pygame.init()

# تنظیمات
WIDTH = 600
HEIGHT = 800
BRICK_WIDTH = 60
BRICK_HEIGHT = 20
PADDLE_WIDTH = 100

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# رنگ‌ها
COLORS = [
    (255, 0, 0),
    (255, 165, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 0, 255)
]

# ایجاد آجرها
bricks = []
for i in range(5):
    for j in range(10):
        bricks.append(pygame.Rect(
            j * (BRICK_WIDTH + 5) + 3,
            i * (BRICK_HEIGHT + 5) + 50,
            BRICK_WIDTH,
            BRICK_HEIGHT
        ))

paddle = pygame.Rect(WIDTH//2 - PADDLE_WIDTH//2, HEIGHT - 40, PADDLE_WIDTH, 10)
ball = pygame.Rect(WIDTH//2 - 10, HEIGHT - 60, 20, 20)
ball_speed = [4, -4]

# حلقه بازی
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # کنترل پدل
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 7
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 7

    # حرکت توپ
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # تشخیص برخورد
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_speed[0] *= -1
    if ball.top <= 0:
        ball_speed[1] *= -1
    if ball.colliderect(paddle):
        ball_speed[1] *= -1

    # برخورد با آجرها
    for brick in bricks[:]:
        if ball.colliderect(brick):
            bricks.remove(brick)
            ball_speed[1] *= -1
            break

    # رسم اجزا
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (255, 255, 255), paddle)
    pygame.draw.ellipse(screen, (255, 255, 255), ball)
    
    for i, brick in enumerate(bricks):
        pygame.draw.rect(screen, COLORS[i//10], brick)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()